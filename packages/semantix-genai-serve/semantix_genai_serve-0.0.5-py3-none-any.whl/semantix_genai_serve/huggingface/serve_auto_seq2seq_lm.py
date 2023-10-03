import os
from abc import ABC, abstractmethod
from typing import Dict, Optional
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from semantix_genai_serve import SemantixTorchKserve

class ServeAutoSeq2SeqLM(SemantixTorchKserve):

    def __init__(self, checkpoint: str, name: Optional[str] = None, base_cache_dir: Optional[str] = None,
                 force_local_load: Optional[bool] = False):
        super().__init__(checkpoint, name, base_cache_dir, force_local_load)

    def load(self, checkpoint: str, base_cache_dir: str, force_local_load: bool):
        if not force_local_load:
            tokenizer_path = checkpoint
            model_path = checkpoint
        else :
            base_cache_dir = os.getenv("BASE_CACHE_DIR", "/mnt/models")
            tokenizer_path = os.path.join(base_cache_dir, "tokenizer")
            model_path = os.path.join(base_cache_dir, "model")
        
        self._tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, local_files_only=force_local_load, device_map={"": self.device})
        self._model = AutoModelForSeq2SeqLM.from_pretrained(model_path, local_files_only=force_local_load, device_map={"": self.device})
        self.ready = True

    @abstractmethod
    def predict(self, payload: Dict, headers: Dict[str, str] = None) -> Dict:
        pass