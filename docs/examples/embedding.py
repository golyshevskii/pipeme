from sentence_transformers import SentenceTransformer, util

# Инициализируем модель Jina Embeddings v3
model = SentenceTransformer(
    "jinaai/jina-embeddings-v3",
    trust_remote_code=True
)

# Пример текстов (наш условный "FAQ-блок")
FAQ_CONTEXTS = [
    "У нас есть собственная система для orchestration пайплайнов данных.",
    "Мы используем Jina Embeddings v3 как модель эмбеддингов.",
    "Система использует MLflow для трекинга экспериментов.",
    "Pipeme работает как AI-ассистент в Telegram.",
    "Для хранения векторов мы используем внутренний векторный стор."
]

# Предобработаем контекст: получим эмбеддинги всех фрагментов
task = "retrieval.query"
faq_embeddings = model.encode(
    FAQ_CONTEXTS,
    task=task,
    prompt_name=task
)

def build_prompt(user_query: str, context_block: str) -> str:
    """
    Формируем промпт для AI на основе найденного контекста.
    """
    prompt = (
        f"Контекст:\n{context_block}\n\n"
        f"Вопрос:\n{user_query}\n\n"
        "Пожалуйста, ответь, используя контекст выше."
    )
    return prompt

def find_best_context(user_query: str, top_k: int = 1) -> str:
    """
    Находим наиболее релевантный фрагмент из FAQ_CONTEXTS
    для пользовательского запроса.
    """
    # Кодируем пользовательский запрос с теми же параметрами
    query_embedding = model.encode(
        [user_query],
        task=task,
        prompt_name=task
    )

    # Считаем косинусную схожесть запроса с нашими фрагментами
    scores = util.cos_sim(query_embedding, faq_embeddings)[0]
    # Выбираем top_k фрагментов по убыванию схожести
    top_results = scores.topk(k=top_k)

    # Склеиваем несколько лучших фрагментов в один блок (если top_k > 1)
    best_contexts = [FAQ_CONTEXTS[idx] for idx in top_results[1]]
    return "\n".join(best_contexts)

def generate_prompt_for_user_query(user_query: str) -> str:
    # Ищем лучший контекст
    context_block = find_best_context(user_query, top_k=1)
    
    # Формируем итоговый промпт
    prompt = build_prompt(user_query, context_block)
    return prompt

if __name__ == "__main__":
    user_input = "Какая модель эмбеддингов используется в нашей системе?"
    prompt_to_ai = generate_prompt_for_user_query(user_input)
    print(prompt_to_ai)

# Вопрос: Какая модель эмбеддингов используется в нашей системе?
# Найденный контекст: Мы используем Jina Embeddings v3 как модель эмбеддингов.
