import unittest
import json
import os
from app import validate_amount, validate_date

class TestAppFunctions(unittest.TestCase):
    TEST_FILE = "test_expenses.json"
    
    def setUp(self):
        # Создаем пустой файл для тестов записи/чтения
        with open(self.TEST_FILE, 'w') as f:
            json.dump([], f)
    
    def tearDown(self):
        # Удаляем тестовый файл после тестов
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)
    
    def test_validate_amount_valid(self):
        """Валидные суммы должны возвращаться как float."""
        self.assertEqual(validate_amount("10"), 10.0)
        self.assertEqual(validate_amount("15.5"), 15.5)
    
    def test_validate_amount_invalid(self):
        """Невалидные суммы должны вызывать ValueError."""
        with self.assertRaises(ValueError) as context:
            validate_amount("-5")
            self.assertIn("больше нуля", str(context.exception))
        
        with self.assertRaises(ValueError) as context:
            validate_amount("abc")
            self.assertIn("корректную сумму", str(context.exception))
    
    def test_validate_date_valid(self):
        """Валидная дата должна возвращаться как объект date."""
        result = validate_date("2026-04-29")
        self.assertEqual(result.isoformat(), "2026-04-29")
    
    def test_validate_date_invalid(self):
        """Невалидная дата должна вызывать ValueError."""
        with self.assertRaises(ValueError) as context:
            validate_date("29-04-2026") # Неверный формат
            self.assertIn("ГГГГ-ММ-ДД", str(context.exception))
        
if __name__ == '__main__':
    unittest.main()
