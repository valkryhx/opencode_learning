#### 这个opencode看不全历史对话，so 我很好奇能否找到它的session来看看
###  OpenCode 的 session 数据存储在 SQLite 数据库中： 它自己找到的 可以让它自己写列出和导出session的py
### 写好之后 让它导出 drawio 相关的session 到本地观看

路径: `C:\Users\drago\.local\share\opencode\`
文件:
- `opencode.db` - 主数据库
- `opencode.db-wal` - Write-Ahead Log  
- `opencode.db-shm` - Shared Memory

这是一个 SQLite 数据库，可以直接用 sqlite3 查看内容。

---

## 导入/导出工具

### Python 脚本

保存为 `show_opencode_session.py`：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import json
from pathlib import Path
import argparse

DB_PATH = r"C:\Users\drago\.local\share\opencode\opencode.db"


def list_sessions(cursor, limit=None, directory=None):
    query = """
        SELECT id, title, directory, time_created, time_updated, version
        FROM session 
        WHERE 1=1
    """
    params = []
    
    if directory:
        query += " AND directory LIKE ?"
        params.append(f"%{directory}%")
    
    query += " ORDER BY time_created DESC"
    
    if limit:
        query += " LIMIT ?"
        params.append(limit)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    print(f"\n{'='*100}")
    print(f"{'ID':<35} | {'Title':<40} | {'Directory':<20} | {'Version'}")
    print(f"{'='*100}")
    
    for row in rows:
        session_id, title, directory, created, updated, version = row
        title_short = title[:38] if title else "None"
        dir_short = directory[:18] if directory else "None"
        print(f"{session_id:<35} | {title_short:<40} | {dir_short:<20} | {version}")
    
    print(f"{'='*100}")
    print(f"Total sessions: {len(rows)}")
    return [row[0] for row in rows]


def get_session_info(cursor, session_id):
    cursor.execute("""
        SELECT id, slug, directory, title, version, time_created, time_updated
        FROM session WHERE id = ?
    """, (session_id,))
    row = cursor.fetchone()
    if not row:
        return None
    return {
        "id": row[0], "slug": row[1], "directory": row[2],
        "title": row[3], "version": row[4],
        "time_created": row[5], "time_updated": row[6]
    }


def get_messages(cursor, session_id):
    cursor.execute("""
        SELECT id, data FROM message WHERE session_id = ? ORDER BY time_created
    """, (session_id,))
    return cursor.fetchall()


def get_parts(cursor, session_id):
    cursor.execute("""
        SELECT id, message_id, data FROM part WHERE session_id = ? ORDER BY time_created
    """, (session_id,))
    return cursor.fetchall()


def parse_part_data(data_str):
    try:
        return json.loads(data_str)
    except json.JSONDecodeError:
        return {"raw": data_str}


def format_conversation(messages, parts):
    message_parts = {}
    for part_id, msg_id, data in parts:
        if msg_id not in message_parts:
            message_parts[msg_id] = []
        message_parts[msg_id].append(parse_part_data(data))

    conversation = []
    for msg_id, data in messages:
        msg_data = parse_part_data(data)
        role = msg_data.get("role", "unknown")
        parts_list = message_parts.get(msg_id, [])
        
        full_text = ""
        reasoning = ""
        tool_calls = []
        
        for part in parts_list:
            part_type = part.get("type", "")
            if part_type == "text":
                full_text += part.get("text", "")
            elif part_type == "reasoning":
                reasoning = part.get("text", "")
            elif part_type == "tool":
                tool_name = part.get("tool", "")
                tool_input = part.get("state", {}).get("input", {})
                tool_calls.append({"tool": tool_name, "input": tool_input})
        
        conversation.append({
            "role": role, "text": full_text, "reasoning": reasoning if reasoning else None,
            "tool_calls": tool_calls if tool_calls else None,
            "model": msg_data.get("model", {}), "finish": msg_data.get("finish"),
            "error": msg_data.get("error")
        })
    
    return conversation


def print_conversation(conversation):
    for i, msg in enumerate(conversation, 1):
        role = msg["role"].upper()
        print(f"\n{'='*50}")
        print(f"消息 #{i} - {role}")
        print(f"{'='*50}")
        
        if msg.get("error"):
            print(f"Error: {msg['error']}")
        
        if msg.get("reasoning"):
            print(f"\nReasoning:\n{msg['reasoning']}")
        
        if msg.get("text"):
            print(f"\nText:\n{msg['text']}")
        
        if msg.get("tool_calls"):
            print(f"\nTool Calls:")
            for tc in msg["tool_calls"]:
                print(f"  - {tc['tool']}: {tc['input']}")


def export_to_markdown(conversation, session_info, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# OpenCode Session Export\n\n")
        f.write(f"**Session ID**: {session_info['id']}\n")
        f.write(f"**Title**: {session_info['title']}\n")
        f.write(f"**Directory**: {session_info['directory']}\n\n---\n\n")
        
        for i, msg in enumerate(conversation, 1):
            role = msg["role"].upper()
            f.write(f"## Message #{i} - {role}\n\n")
            
            if msg.get("error"):
                f.write(f"**Error**: {msg['error']}\n\n")
            if msg.get("reasoning"):
                f.write(f"**Reasoning**:\n{msg['reasoning']}\n\n")
            if msg.get("text"):
                f.write(f"**Text**:\n{msg['text']}\n\n")
            if msg.get("tool_calls"):
                f.write("**Tool Calls**:\n")
                for tc in msg["tool_calls"]:
                    f.write(f"- {tc['tool']}: {tc['input']}\n")
                f.write("\n")
            f.write("---\n\n")


def main():
    parser = argparse.ArgumentParser(description="OpenCode Session Import/Export Tool")
    parser.add_argument("--list", "-l", action="store_true", help="List all sessions")
    parser.add_argument("--limit", "-n", type=int, default=None, help="Number of sessions to list")
    parser.add_argument("--directory", "-d", type=str, help="Filter sessions by directory")
    parser.add_argument("--session-id", "-s", type=str, help="Session ID to export")
    parser.add_argument("--output", "-o", type=str, help="Output file path")
    
    args = parser.parse_args()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if args.list:
        list_sessions(cursor, args.limit, args.directory)
        conn.close()
        return
    
    session_id = args.session_id
    if not session_id:
        session_id = list_sessions(cursor, 10, args.directory)[0]
        print(f"\nUsing latest session: {session_id}")
    
    session_info = get_session_info(cursor, session_id)
    messages = get_messages(cursor, session_id)
    parts = get_parts(cursor, session_id)
    conversation = format_conversation(messages, parts)
    
    print_conversation(conversation)
    
    output_path = args.output if args.output else Path(__file__).parent / "session_export.md"
    export_to_markdown(conversation, session_info, output_path)
    print(f"\nExported to: {output_path}")
    
    conn.close()


if __name__ == "__main__":
    main()
```

### 使用方法

```bash
# 列出所有 session (默认显示最新 50 个)
python show_opencode_session.py --list

# 限制显示数量
python show_opencode_session.py --list -n 10

# 按目录过滤
python show_opencode_session.py --list -d google_plugin

# 导出指定 session
python show_opencode_session.py -s ses_323acb6eaffeS2a1GBHzG3GRV4 -o output.md

# 列出并过滤，然后导出最新的
python show_opencode_session.py --list -d opencode_learning
```

### 数据库表结构

```sql
-- session 表
CREATE TABLE session (
    id text PRIMARY KEY,
    project_id text NOT NULL,
    parent_id text,
    slug text NOT NULL,
    directory text NOT NULL,
    title text NOT NULL,
    version text NOT NULL,
    share_url text,
    time_created integer NOT NULL,
    time_updated integer NOT NULL,
    workspace_id text
);

-- message 表 (每条对话)
CREATE TABLE message (
    id text PRIMARY KEY,
    session_id text NOT NULL,
    time_created integer NOT NULL,
    time_updated integer NOT NULL,
    data text NOT NULL
);

-- part 表 (消息的具体内容)
CREATE TABLE part (
    id text PRIMARY KEY,
    message_id text NOT NULL,
    session_id text NOT NULL,
    time_created integer NOT NULL,
    time_updated integer NOT NULL,
    data text NOT NULL
);
```