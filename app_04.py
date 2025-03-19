aimiessage = AIMessage(
    content = '실행했습니다.', 
    add_messages = {'refusal': None},
    response_metadata = {
        'token_usage': {
            'completion_tokens': 243,
            'prompt_tokens': 21,
            'total_tokens': 264, 
            'completion_tokens_details': {
                'accepted_prediction_tokens': 0,
                'audio_tokens': 0,
                'reasoning_tokens': 0, 
                'rejected_prediction_tokens': 0 
            },
            'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
        }, 
        'model_name': 'gpt-4o-mini-2024-07-18', 
        'system_fingerprint': 'fp_b8bc95a0ac', 
        'finish_reason': 'stop', 
        'logprobs': None
    },
    id='run-058fd8e4-aeb3-4ff1-9951-fde8f3327a2f-1',
    usage_metadata = {
    'input_tokens': 21, 
    'output_tokens': 243, 
    'total_tokens': 264, 
    'input_token_details': {'audio': 0, 'cache_read': 0}, 
    'output_token_details': {'audio': 0, 'reasoning': 0}
    } 
)
