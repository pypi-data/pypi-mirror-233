import logging
from typing import Any, Dict
from Mama.utils import get_db, save_db


class Configuration() :

    def __init__(self, initial_config=None):
        self.config = None
        self.prompt_template = ""
        self.input_variables = []
        self.db_name = ""
        try:
            self.load()
        except Exception as e:
            print(f"Error Loading Configuration {e}")
    
    def load(self, db_name) :
        logging.basicConfig(format='[%(asctime)s]::[%(levelname)s - %(funcName)s]:: %(message)s', filename='flask.log', level=logging.DEBUG)

        self.db_name = db_name
        db = get_db(db_name)
        if not db:
            return False
        
        self.config = db.get("config")
        if not self.config:
            logging.info(f"No configuration session found in database")
            return False
        
        logging.info(f"Configuration: {self.config}")
        return True
    
    def get(self, name : str) -> Any:
        if not self.config:
            return ""
        return self.config.get(name, [])
    
    def set(self, name : str, data : Any):
        if not self.config:
            return
        self.config[name] = data
        self.save()
    
    def save(self):
        db = get_db(self.db_name)
        if not db:
            return False
        
        db["config"] = self.config
        save_db(self.db_name, db)

    def get_llm_params(self, model) -> Dict[str, Any]:      
        db = get_db(self.db_name)
        if not db:
            return {}
        
        LLMs = db.get("LLMs", [])
        if not LLMs:
            return {}
        
        for llm in LLMs:
            if model == llm.get("model", ""):
                self.prompt_template = llm.get("prompt_template", "")
                self.input_variables = llm.get("input_variables", "")
                return llm.get("parameters", {})
        return {}
    
    def add_chatbot(self, chatbot : Dict) :
        db = get_db(self.db_name)
        if not db:
            return {}
        
        cbs = db.get("CHATBOT", [])
        if not cbs:
            cbs = [chatbot]
        else:
            cbs.append(chatbot)
        db["CHATBOT"] = cbs

        save_db(self.db_name, db)
        
    def get_prompt_template(self):
        return self.prompt_template
    
    def get_input_variables(self):
        return self.input_variables
        


    