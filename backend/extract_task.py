import os
from datetime import datetime
from typing import Optional

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, ValidationError


class Task(BaseModel):
    task_name: str
    start_time: datetime
    end_time: datetime


def extract_task(text: str) -> Optional[Task]:
    """
    テキストからLLMを用いてタスクを抽出する

    Args:
        text (str): テキスト

    Returns:
        Task|None: 抽出したタスク
    """
    # APIキーの取得
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("環境変数GEMINI_API_KEYが設定されていません")
        return None

    # LangChain Geminiモデルの初期化
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro", google_api_key=api_key, temperature=0.1
    )

    # Pydanticパーサーの設定
    parser = PydanticOutputParser(pydantic_object=Task)

    # プロンプトの作成
    prompt_template = """
    以下のテキストからタスク情報を抽出してください。
    
    テキスト: {text}
    
    必ずタスク名、開始時間、終了時間の3つの情報を抽出してください。
    日時はISO 8601形式（例：2023-05-10T10:00:00）で出力してください。
    
    もし与えられたテキストにタスクに関連する情報が含まれていない場合は、「タスク情報なし」と明示してください。
    
    {format_instructions}
    """

    # プロンプトの設定
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["text"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    try:
        # プロンプトのフォーマット
        formatted_prompt = prompt.format(text=text)

        # LLMからの回答取得
        response = llm.invoke(formatted_prompt)
        content = response.content

        # タスク情報がない場合の処理
        if "タスク情報なし" in str(content):
            return None

        # 回答を解析
        try:
            return parser.parse(str(content))
        except ValidationError:
            print("タスク情報の解析に失敗しました")
            return None

    except Exception as e:
        print(f"タスク抽出エラー: {e}")
        return None
