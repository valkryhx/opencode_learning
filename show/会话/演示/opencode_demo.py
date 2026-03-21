# opencode-ai SDK 调用演示
# 依赖：pip install opencode-ai
# 前提：opencode serve --port 4096 已在后台运行

import os
from opencode_ai import Opencode

# 连接到本地 opencode 服务
client = Opencode(base_url="http://127.0.0.1:4096")


def demo_list_sessions():
    """列出所有会话"""
    print("=" * 50)
    print("[1] 列出最近 5 个会话")
    print("=" * 50)
    sessions = client.session.list()
    for i, s in enumerate(sessions[:5]):
        print(f"  {i+1}. {s.id}")
        print(f"     标题: {s.title[:50] if s.title else '(无标题)'}...")
        print()


def demo_session_operations():
    """演示会话的增删查操作"""
    print("=" * 50)
    print("[2] 会话创建、查询、删除")
    print("=" * 50)

    import httpx, json

    # 创建新会话
    r = httpx.post("http://127.0.0.1:4096/session", json={})
    session = r.json()
    session_id = session["id"]
    print(f"  新会话 ID: {session_id}")
    print(f"  slug: {session.get('slug')}")
    print(f"  创建时间: {session.get('time', {}).get('created')}")

    # 查询该会话的消息列表（空会话）
    msgs = httpx.get(f"http://127.0.0.1:4096/session/{session_id}/message").json()
    print(f"  消息数量: {len(msgs) if isinstance(msgs, list) else '?'}")

    # 删除会话
    del_r = httpx.delete(f"http://127.0.0.1:4096/session/{session_id}")
    print(f"  删除状态: {del_r.status_code}")
    print(f"  会话已删除: {session_id}")


def demo_existing_session_messages():
    """读取现有会话的消息"""
    print("=" * 50)
    print("[3] 读取现有会话最近消息")
    print("=" * 50)

    import httpx

    # 取当前活跃会话（第一个）
    sessions = client.session.list()
    if not sessions:
        print("  无会话")
        return

    session_id = sessions[0].id
    print(f"  会话: {session_id}")
    print(f"  标题: {sessions[0].title[:60] if sessions[0].title else '(无标题)'}")

    # 获取消息
    msgs_resp = httpx.get(f"http://127.0.0.1:4096/session/{session_id}/message")
    msgs = msgs_resp.json()
    if isinstance(msgs, list):
        print(f"  总消息数: {len(msgs)}")
        # 显示最后 2 条消息的摘要
        for msg in msgs[-2:]:
            role = msg.get("role", "?")
            parts = msg.get("parts", [])
            text = next((p.get("text", "")[:80] for p in parts if p.get("type") == "text"), "(非文本)")
            print(f"  [{role}]: {text}...")
    else:
        print(f"  响应: {str(msgs)[:200]}")


def demo_get_messages():
    """获取现有会话的消息"""
    print("=" * 50)
    print("[3] 获取当前会话的最近 3 条消息")
    print("=" * 50)

    sessions = client.session.list()
    if not sessions:
        print("  没有找到会话")
        return

    # 取第一个会话
    session_id = sessions[0].id
    print(f"  会话 ID: {session_id}")

    messages = client.session.messages(session_id)
    recent = list(messages)[-3:] if len(list(messages)) > 3 else list(messages)
    for msg in recent:
        role = getattr(msg, 'role', '?')
        print(f"  [{role}] {str(msg)[:100]}")


def demo_chat():
    """创建新会话并发送消息，演示 chat API"""
    print("=" * 50)
    print("[3] Chat 演示：发送消息并获取 AI 回复")
    print("=" * 50)

    import httpx

    # 创建会话
    ses = httpx.post("http://127.0.0.1:4096/session", json={}, timeout=10).json()
    session_id = ses["id"]
    print(f"  新会话 ID: {session_id}")

    # 发送消息（服务端使用 config.json 中配置的默认模型）
    print("  发送消息: '用一句话介绍你自己'")
    resp = httpx.post(
        f"http://127.0.0.1:4096/session/{session_id}/message",
        json={"parts": [{"type": "text", "text": "用一句话介绍你自己"}]},
        timeout=120,
    ).json()

    info = resp.get("info", {})
    print(f"  Provider: {info.get('providerID')}")
    print(f"  Model: {info.get('modelID')}")

    if info.get("error"):
        print(f"  错误: {info['error']}")
    else:
        for p in resp.get("parts", []):
            if p.get("type") == "text":
                print(f"  AI 回复: {p['text'][:300]}")

    # 清理
    httpx.delete(f"http://127.0.0.1:4096/session/{session_id}")
    print(f"  会话已删除: {session_id}")


if __name__ == "__main__":
    try:
        demo_list_sessions()
        demo_session_operations()
        demo_chat()
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
