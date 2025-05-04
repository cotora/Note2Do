import os
from datetime import datetime
from typing import List

from dotenv import load_dotenv
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, ValidationError


class Task(BaseModel):
    """
    タスク情報
    """

    task_name: str
    start_time: datetime
    end_time: datetime


class TaskList(BaseModel):
    """
    タスク情報のリスト
    """

    tasks: List[Task]


def extract_task(text: str) -> List[Task]:
    """
    テキストからLLMを用いてタスクを抽出する

    Args:
        text (str): テキスト

    Returns:
        List[Task]: 抽出したタスクのリスト
    """
    # APIキーの取得
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("環境変数GEMINI_API_KEYが設定されていません")
        return []

    # LangChain Geminiモデルの初期化
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash", google_api_key=api_key, temperature=0.1
    )

    # Pydanticパーサーの設定
    parser = PydanticOutputParser(pydantic_object=TaskList)

    # プロンプトの作成
    prompt_template = """
    以下のテキストから全てのタスク情報を抽出してください。
    
    テキスト: {text}
    
    各タスクごとに、タスク名、開始時間、終了時間の3つの情報を抽出してください。
    日時はISO 8601形式（例：2023-05-10T10:00:00）で出力してください。
    
    複数のタスクが含まれている場合は、全てのタスクを抽出してください。
    もし与えられたテキストにタスクに関連する情報が含まれていない場合は、空のタスクリストを返してください。
    
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
            return []

        # 回答を解析
        try:
            task_list = parser.parse(str(content))
            return task_list.tasks
        except ValidationError as e:
            print(f"タスク情報の解析に失敗しました: {e}")
            return []

    except Exception as e:
        print(f"タスク抽出エラー: {e}")
        return []


if __name__ == "__main__":
    text = """
    ポスターセッションは5月15日（木）18:00〜20:00に学内カフェテリアにて実施予定です。
    参加希望者は5月10日（土）までに応募フォームから登録をお願いいたします。
    また、全体ミーティングは5月12日（月）10:00〜11:30に会議室Aで行います。
    """
    tasks = extract_task(text)
    for i, task in enumerate(tasks):
        print(f"タスク {i + 1}:")
        print(f"  タスク名: {task.task_name}")
        print(f"  開始時間: {task.start_time}")
        print(f"  終了時間: {task.end_time}")
        print()
