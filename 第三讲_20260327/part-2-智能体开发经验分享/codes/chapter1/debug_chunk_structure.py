#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
诊断脚本：查看流式输出中 chunk 的结构差异
"""

import os
import json
import yaml
import sys
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def load_credentials():
    path = Path("private_key.yaml")
    if not path.exists():
        path = Path(__file__).resolve().parents[3] / "private_key.yaml"
    
    if not path.exists():
        raise FileNotFoundError(f"Cannot find private_key.yaml")
        
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

try:
    config = load_credentials()
    client = OpenAI(
        api_key=config.get("test_api_key"),
        base_url=config.get("test_api_base")
    )
    model_name = config.get("test_model", "stepfun-ai/step-3.5-flash")
    print(f"Using model: {model_name}")
    print(f"Base URL: {config.get('test_api_base')}")
    print("="*60)
except Exception as e:
    print(f"Error loading credentials: {e}")
    sys.exit(1)

TOOL_DESC = """
你可以使用以下工具。如果你想使用工具，请只输出一个 JSON 对象，格式如下：
{
    "tool": "tool_name",
    "args": {
        "arg_name": "value"
    }
}

可用工具：
1. calculate: 计算数学表达式。参数: expression (string)
"""

def diagnose_stream():
    messages = [
        {"role": "system", "content": f"你是一个智能助手。\n{TOOL_DESC}"},
        {"role": "user", "content": "帮我算一下 123 乘以 456 是多少"}
    ]
    
    print("Starting stream diagnosis...\n")
    
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        stream=True 
    )
    
    chunk_count = 0
    empty_choices_count = 0
    
    for chunk in response:
        chunk_count += 1
        
        # 检查 chunk 结构
        print(f"\n--- Chunk #{chunk_count} ---")
        print(f"Chunk type: {type(chunk)}")
        print(f"Chunk dict keys: {chunk.__dict__.keys() if hasattr(chunk, '__dict__') else 'N/A'}")
        
        # 检查 choices
        if hasattr(chunk, 'choices'):
            print(f"chunk.choices type: {type(chunk.choices)}")
            print(f"chunk.choices length: {len(chunk.choices)}")
            
            if len(chunk.choices) == 0:
                empty_choices_count += 1
                print("⚠️  WARNING: chunk.choices is EMPTY!")
                print(f"Full chunk: {chunk}")
            else:
                choice = chunk.choices[0]
                print(f"choice type: {type(choice)}")
                print(f"choice.delta: {choice.delta}")
                if hasattr(choice.delta, 'content'):
                    print(f"choice.delta.content: {repr(choice.delta.content)}")
                else:
                    print("⚠️  choice.delta has no 'content' attribute")
        else:
            print("⚠️  chunk has no 'choices' attribute!")
            print(f"Full chunk: {chunk}")
    
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Total chunks: {chunk_count}")
    print(f"  Empty choices chunks: {empty_choices_count}")
    print(f"  Problematic ratio: {empty_choices_count/chunk_count*100:.1f}%" if chunk_count > 0 else "N/A")

if __name__ == "__main__":
    diagnose_stream()
