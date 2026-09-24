import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { COURSES, ZJUAM } from 'login-zju';

const TODO_URL = 'https://courses.zju.edu.cn/api/todos?no-intercept=true';
const DATA_DIR = new URL('../data/', import.meta.url);
const TODOS_FILE = new URL('../data/zju_todos.json', import.meta.url);
const CHANGES_FILE = new URL('../data/zju_changes.json', import.meta.url);

const username = process.env.ZJU_USERNAME;
const password = process.env.ZJU_PASSWORD;

if (!username || !password) {
  throw new Error('Missing ZJU credentials. Configure repository secrets ZJU_USERNAME and ZJU_PASSWORD.');
}

const cleanText = (value) => {
  if (typeof value !== 'string') return '';
  return value
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/gi, ' ')
    .replace(/&amp;/gi, '&')
    .replace(/&lt;/gi, '<')
    .replace(/&gt;/gi, '>')
    .replace(/&#39;/gi, "'")
    .replace(/&quot;/gi, '"')
    .replace(/\s+/g, ' ')
    .trim();
};

const collectText = (node, out = [], depth = 0) => {
  if (depth > 8 || node == null) return out;
  if (Array.isArray(node)) {
    for (const item of node) collectText(item, out, depth + 1);
    return out;
  }
  if (typeof node !== 'object') return out;

  const preferred = new Set([
    'description','content','instruction','instructions','body',
    'intro','introduction','requirement','requirements','remark','remarks'
  ]);

  for (const [key, value] of Object.entries(node)) {
    if (preferred.has(key.toLowerCase()) && typeof value === 'string') {
      const text = cleanText(value);
      if (text && !out.includes(text)) out.push(text);
    }
    if (typeof value === 'object' && value !== null) {
      collectText(value, out, depth + 1);
    }
  }
  return out;
};

const collectAttachmentNames = (node, out = [], depth = 0) => {
  if (depth > 10 || node == null) return out;
  if (Array.isArray(node)) {
    for (const item of node) collectAttachmentNames(item, out, depth + 1);
    return out;
  }
  if (typeof node !== 'object') return out;

  for (const [key, value] of Object.entries(node)) {
    if (
      typeof value === 'string' &&
      ['name','filename','file_name','title'].includes(key.toLowerCase()) &&
      /\.(pptx?|pdf|docx?|xlsx?|zip)$/i.test(value.trim())
    ) {
      const name = value.trim();
      if (!out.includes(name)) out.push(name);
    }
    if (typeof value === 'object' && value !== null) {
      collectAttachmentNames(value, out, depth + 1);
    }
  }
  return out;
};

const stableKey = (todo) => String(todo.source_id ?? todo.title ?? '');

const normalizeTodo = async (courses, todo) => {
  let detail = null;
  let detailFetchError = null;

  try {
    if (todo.id != null) {
      const isExam = String(todo.type ?? '').toLowerCase().includes('exam');
      const url = isExam
        ? `https://courses.zju.edu.cn/api/exams/${todo.id}`
        : `https://courses.zju.edu.cn/api/activities/${todo.id}?sub_course_id=0`;
      const response = await courses.fetch(url);
      if (response.ok) detail = await response.json();
      else detailFetchError = `HTTP ${response.status}`;
    }
  } catch (error) {
    detailFetchError = error instanceof Error ? error.message : String(error);
  }

  return {
    source_id: todo.id ?? null,
    course_id: todo.course_id ?? null,
    course_name: todo.course_name ?? null,
    course_code: todo.course_code ?? null,
    title: todo.title ?? null,
    type: todo.type ?? null,
    end_time: todo.end_time ?? null,
    is_locked: todo.is_locked ?? null,
    detail_text: collectText(detail).join(' ').slice(0, 6000) || null,
    attachment_names: collectAttachmentNames(detail).slice(0, 50),
    detail_fetch_error: detailFetchError,
    source_url:
      todo.course_id != null && todo.id != null
        ? `https://courses.zju.edu.cn/course/${todo.course_id}/learning-activity#/${todo.id}`
        : null
  };
};

const readPrevious = async () => {
  try {
    const parsed = JSON.parse(await readFile(TODOS_FILE, 'utf8'));
    return Array.isArray(parsed.todos) ? parsed.todos : [];
  } catch {
    return [];
  }
};

await mkdir(DATA_DIR, { recursive: true });

const courses = new COURSES(new ZJUAM(username, password));
const response = await courses.fetch(TODO_URL);
if (!response.ok) throw new Error(`Failed to fetch 学在浙大 todos: HTTP ${response.status}`);

const payload = await response.json();
const rawTodos = Array.isArray(payload?.todo_list) ? payload.todo_list : [];

const todos = [];
for (const todo of rawTodos) todos.push(await normalizeTodo(courses, todo));

todos.sort((a, b) => {
  const ta = a.end_time ? Date.parse(a.end_time) : Number.POSITIVE_INFINITY;
  const tb = b.end_time ? Date.parse(b.end_time) : Number.POSITIVE_INFINITY;
  if (ta !== tb) return ta - tb;
  return String(a.course_name ?? '').localeCompare(String(b.course_name ?? ''), 'zh-CN');
});

const previous = await readPrevious();
const oldMap = new Map(previous.map((item) => [stableKey(item), item]));
const newMap = new Map(todos.map((item) => [stableKey(item), item]));

const added = [];
const updated = [];
const removed = [];

for (const [key, item] of newMap) {
  if (!oldMap.has(key)) added.push(item);
  else if (JSON.stringify(oldMap.get(key)) !== JSON.stringify(item)) {
    updated.push({ before: oldMap.get(key), after: item });
  }
}
for (const [key, item] of oldMap) if (!newMap.has(key)) removed.push(item);

await writeFile(TODOS_FILE, JSON.stringify({ todos }, null, 2) + '\n', 'utf8');
await writeFile(CHANGES_FILE, JSON.stringify({ added, updated, removed }, null, 2) + '\n', 'utf8');

console.log(`Synced ${todos.length} todos. added=${added.length}, updated=${updated.length}, removed=${removed.length}`);
