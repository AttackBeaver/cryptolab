import importlib
import pkgutil
import inspect
from modules.base_module import CryptoModule
from typing import Dict, List, Type

class ModuleLoader:
    def __init__(self):
        self.modules: Dict[str, CryptoModule] = {}
        self.categories: Dict[str, List[str]] = {}
    
    def discover_modules(self) -> Dict[str, CryptoModule]:
        """Автоматически находит и загружает все модули в пакете modules"""
        self.modules = {}
        
        # Сканируем все подпакеты в modules
        package_path = 'modules'
        package = importlib.import_module(package_path)
        
        for importer, module_name, ispkg in pkgutil.walk_packages(package.__path__, package.__name__ + '.'):
            if ispkg:
                # Это пакет (папка), сканируем его содержимое
                self._load_modules_from_package(module_name)
        
        # Сортируем модули по категориям
        self._categorize_modules()
        
        return self.modules
    
    def _load_modules_from_package(self, package_name: str):
        """Загружает модули из указанного пакета"""
        try:
            package = importlib.import_module(package_name)
            
            for importer, module_name, ispkg in pkgutil.walk_packages(
                package.__path__, package.__name__ + '.'
            ):
                if not ispkg:
                    # Это файл модуля, загружаем его
                    self._load_single_module(module_name)
                    
        except ImportError as e:
            print(f"Ошибка загрузки пакета {package_name}: {e}")
    
    def _load_single_module(self, module_name: str):
        """Загружает один модуль и находит в нем классы CryptoModule"""
        try:
            module = importlib.import_module(module_name)
            
            # Ищем все классы в модуле, которые являются подклассами CryptoModule
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if (issubclass(obj, CryptoModule) and 
                    obj != CryptoModule and 
                    obj.__module__ == module_name):
                    
                    # Создаем экземпляр модуля
                    try:
                        module_instance = obj()
                        module_id = self._generate_module_id(module_instance)
                        
                        if module_id not in self.modules:
                            self.modules[module_id] = module_instance
                            print(f"✅ Загружен модуль: {module_instance.name} ({module_id})")
                        else:
                            print(f"⚠️ Дубликат модуля: {module_instance.name}")
                            
                    except Exception as e:
                        print(f"❌ Ошибка создания модуля {name}: {e}")
                        
        except Exception as e:
            print(f"❌ Ошибка загрузки модуля {module_name}: {e}")
    
    def _generate_module_id(self, module: CryptoModule) -> str:
        """Генерирует ID модуля на основе его имени"""
        # Преобразуем имя модуля в snake_case
        name = module.name.lower()
        name = ''.join(c if c.isalnum() else ' ' for c in name)
        words = name.split()
        return '_'.join(words)
    
    def _categorize_modules(self):
        """Сортирует модули по категориям"""
        self.categories = {}
        
        for module_id, module in self.modules.items():
            category = module.category
            if category not in self.categories:
                self.categories[category] = []
            self.categories[category].append(module_id)
        
        # Сортируем категории и модули внутри категорий
        for category in self.categories:
            self.categories[category].sort(
                key=lambda mid: self.modules[mid].name
            )
    
    def get_modules_by_category(self) -> Dict[str, List[CryptoModule]]:
        """Возвращает модули сгруппированные по категориям"""
        categorized = {}
        for category, module_ids in self.categories.items():
            categorized[category] = [
                self.modules[module_id] for module_id in module_ids
            ]
        return categorized
    
    def get_module_categories(self) -> List[str]:
        """Возвращает список всех категорий"""
        return sorted(self.categories.keys())