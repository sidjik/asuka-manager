import ollama
import asyncio
from ollama import Client



class OllamaModel():
    

    def __init__(self, model_name, first_system_message='You are a helpful assistant!'): 
        self.__client = Client(host='ollama:11434')
        self.__model_name = None
        self.__history_limit = 3
        if ':' not in model_name: 
            model_name = model_name.lower() + ':latest'
        for i in self.__client.list()['models']: 
            #if i['name'].split(':')[0].lower() == model_name.lower():
            if i['model'].lower() == model_name.lower(): 
                self.__model_name = i['model']
                self.__model_info = i
                
        if self.__model_name is None: 
            raise ValueError(f"In OllamaModel you entered an incorrect model name - {model_name}")

        

        # Сообщение с ролью 'system' может быть отправлено в самом начале, чтобы задать начальные настройки или тон разговора. Например, можно дать ассистенту инструкции по стилю ответа или уточнить, какие задачи он должен выполнять.

        self.__messages = [{
                'role': 'system', 
                'content': first_system_message,
            }]

        #self.__options = ollama._types.Options(
        self.__options = {
                #Параметры связанные с загрузкой модели(load time options)
                
                'numa': True, # Включает или отключает NUMA (Non-Uniform Memory Access) для оптимизации работы с памятью на многопроцессорных системах.
                'num_ctx': 40960, # Устанавливает размер контекстного окна для генерации следующего токена (размер истории, с которой модель работает).
                #'num_batch': 210, # Размер батча (количество примеров, обрабатываемых одновременно) при обучении или генерации.
                #'num_gpu': int, # Количество используемых графических процессоров (GPU).
                #'main_gpu': int, # Индекс основного графического процессора, который будет использоваться для вычислений.
                #'low_vram': bool, # Включает режим с низким потреблением видеопамяти (VRAM), оптимизируя работу на системах с ограниченным количеством VRAM.
                'f16_kv': True, # Включает использование 16-битных значений (float16) для уменьшения объёма памяти, потребляемой ключевыми значениями (key-value pairs).
                #'logist_all': bool, # Включает логиты для всех шагов генерации, а не только для последнего шага.
                #'vocab_only': bool, # Если включено, используется только словарь (vocabulary) модели без генерации текста. Может быть полезно для анализа модели.
                'use_mmap': True, # Использует memory-mapped файл для оптимизации работы с большими моделями, загружаемыми в память.
                #'use_mlock': bool, # Блокирует модель в оперативной памяти для предотвращения её выгрузки операционной системой.
                #'embedding_only': bool, # Включает режим, в котором используются только эмбеддинги модели без генерации текста.
                #'num_thread': int, # Кол-во потоков используемых для вычесления


                # Параметры времени выполнения(runtime options)

                'num_keep': 40960, # Указывает количество токенов, которые следует сохранить при генерации текста (например, для сохранения определённой части контекста). Очень важно!!!!
                'seed': 21, # Устанавливает начальное значение для генерации случайных чисел. Позволяет делать предсказания вAnalyze the following patient record and identify the diagnosis.  
                #'num_predict': 25, # Максимальное количество токенов для предсказания. Значение `-1` позволяет бесконечную генерацию.
                #'top_k': int, # Ограничивает количество токенов, которые могут быть выбраны моделью на каждом шаге. Чем выше значение, тем больше разнообразие в ответах.
                #'top_p': float, # Используется для nucleus sampling (семплирование по вероятности). Указывает долю вероятности, которую модель будет учитывать при генерации.
                #'tfs_z': float, # Tail free sampling Уменьшает влияние маловероятных токенов на вывод.
                #'typical_p': float, # Указывает на типичную вероятность, чтобы сбалансировать разнообразие и качество текста.
                #'repeat_last_n': -1, # Задаёт количество токенов, которое модель должна учитывать, чтобы избежать повторений. -1 означает использование всего контекста.
                'temperature': 0, # Контролирует креативность модели. Высокие значения делают ответы более разнообразными, низкие — более предсказуемыми.
                #'repeat_penalty': float, # Устанавливает степень наказания за повторение. Чем выше значение, тем сильнее штраф за повторяющиеся фразы.
                #'presence_penalty': float, # Контролирует наличие новых токенов в выводе, повышая вероятность появления новых слов.
                #'frequency_penalty': float, # Контролирует частоту появления токенов, уменьшая вероятность повторения часто встречающихся слов.
                #'mirostat': int, # Включает алгоритм **Mirostat** для контроля за перплексией текста. 0 — отключён, 1 — включён, 2 — Mirostat 2.0.
                #'miro  stat_tau': float, # Контролирует баланс между связанностью и разнообразием текста.
                #'mirostat_eta': float, # Регулирует скорость отклика Mirostat. Высокое значение делает модель более отзывчивой.
                #'penalize_newline': bool, # Определяет нужно ли штрафовать за появление новой строки в тексте
                #'stop' : Sequence[str] # Последовательности которые прерывают генерацию текста. Модель остановиться когда встретит одну из этих последовательностей
            }#, total=False)


    
    def load_model(self): 

        print("load ollama model")


    async def get_response_with_image(self, query, images, keep_alive=360): 
        query = {
            'role' : 'user', 
            'content' : query, 
            'images' : images,
        }
        self.__messages.append(query)
        response = self.__client.chat(model=self.__model_name, 
                               messages = self.__messages[-self.__history_limit*2:], 
                               #messages = [query],
                               tools = None,
                               options = self.__options, 
                               keep_alive = keep_alive, stream=True)

        answer = ''
        for i in response:
            answer += i['message']['content']
            yield i['message']['content']


        answer = {'role': 'assistant', 'content': answer}
        self.__messages.append(answer)


    async def get_response(self, query, keep_alive=360): 
        
        query = {'role': 'user', 'content': query}
        self.__messages.append(query)

        response = self.__client.chat(model=self.__model_name, 
                               messages = self.__messages[-self.__history_limit*2:], 
                               tools = None,
                               options = self.__options, 
                               keep_alive = keep_alive, stream=True)

        answer = ''
        for i in response:
            answer += i['message']['content']
            yield i['message']['content']
            await asyncio.sleep(0.1)
            
        answer = {'role': 'assistant', 'content': answer}
        self.__messages.append(answer)
        #return response['message']['content']


    def get_RAGresponse(self, query, tools): 
        message = self.make_RAGmessage(query, tools)
        response = self.__client.chat(model=self.__model_name, 
                               messages = message, 
                               tools = None,
                               options = self.__options, 
                               keep_alive = 360, stream=True)
        for i in response:
            yield i['message']['content']
        #return response['message']['content']




    def make_RAGmessage(self, query, tools, 
                        system_message="Use the provided documents in tools as your primary reference to answer the user’s questions, drawing directly from their content."): 
        
        if tools is None or len(tools) == 0 or not isinstance(tools, list): 
            raise ValueError("You have tools with value None or length 0.")
        elif query is None or len(query) == 0 or not isinstance(query, str): 
            raise ValueError("You have tools with value None or length 0.")
        
        rag_message = [{'role': 'system', 'content': query}]

        for i in tools: 
            if i is None or i.strip() == '': 
                raise ValueError("You have empty value on tools list.")
            rag_message.append({'role': 'user', 'content': i})

        rag_message.append({'role': 'user', 'content': query})
        
        return rag_message





    def sync_get_response_with_image(self, query, images, keep_alive=360): 
        query = {
            'role' : 'user', 
            'content' : query, 
            'images' : images,
        }
        self.__messages.append(query)
        response = self.__client.chat(model=self.__model_name, 
                               messages = self.__messages[-self.__history_limit*2:], 
                               #messages = [query],
                               tools = None,
                               options = self.__options, 
                               keep_alive = keep_alive)



        return response['message']['content']   
        answer = {'role': 'assistant', 'content': answer}
        self.__messages.append(answer)


    def sync_get_response(self, query, keep_alive=360): 
        
        query = {'role': 'user', 'content': query}
        self.__messages.append(query)

        response = self.__client.chat(model=self.__model_name, 
                               messages = self.__messages[-self.__history_limit*2:], 
                               tools = None,
                               options = self.__options, 
                               keep_alive = keep_alive)

        return response['message']['content']   
        answer = {'role': 'assistant', 'content': answer}
        self.__messages.append(answer)
 

    def append_message(self, role, content):
        self.__messages.append(
            {'role': role, 'content': content}
        )










    def get_model_info(self): 
        return self.__model_info


    def get_messages(self): 
        return self.__messages



    @property
    def options(self): return self.__options
    @options.setter
    def options(self, value): 
        self.__options = value
        for i in self.__options: 
            if i == 'history_limit':
                self.__history_limit = self.__options[i]
                del self.__options[i]
                continue 
            self.__options[i] = int(self.__options[i])




    @property
    def name(self): return self.__model_name


    @property
    def client(self): return self.__client


