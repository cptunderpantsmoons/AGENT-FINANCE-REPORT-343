        # Model Selection
        if api_key:
            st.markdown("#### Model Selection")
            
            # Available models organized by category
            all_models = [
                "x-ai/grok-4.1-fast",
                "google/gemini-2.5-flash-lite",
                "openai/gpt-4.1-nano",
                "openai/gpt-5-mini",
                "nvidia/nemotron-nano-12b-v2-vl",
                "openai/gpt-4o",
                "openai/gpt-4-turbo",
                "anthropic/claude-3.5-sonnet",
                "anthropic/claude-3-haiku",
                "qwen/qwen3-embedding-8b",  # Added Qwen embedding model
            ]
            
            # Initialize model config in session state
            if 'ai_model_config' not in st.session_state:
                st.session_state.ai_model_config = {
                    'validation': 'x-ai/grok-4.1-fast',
                    'extraction': 'nvidia/nemotron-nano-12b-v2-vl',
                    'cross_validation': 'google/gemini-2.5-flash-lite',
                    'note_generation': 'openai/gpt-4.1-nano',
                    'tax_validation': 'google/gemini-2.5-flash-lite',
                    'document_analysis': 'qwen/qwen3-embedding-8b',  # Added for document analysis
                }