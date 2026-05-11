#include <iostream>
#include <sqlite3.h> // Подключаем заголовочный файл
#include <string>
#include <windows.h>

std::string ToUtf8(const std::string& str) {
    if (str.empty()) return "";

    // 1. Определяем размер для временного буфера в UTF-16 (wchar_t)
    int wchars_num = MultiByteToWideChar(1251, 0, str.c_str(), -1, nullptr, 0);
    if (wchars_num == 0) return "";

    std::wstring wstr(wchars_num, 0);
    MultiByteToWideChar(1251, 0, str.c_str(), -1, &wstr[0], wchars_num);

    // 2. Определяем размер для финальной строки в UTF-8
    int chars_num = WideCharToMultiByte(CP_UTF8, 0, wstr.c_str(), -1, nullptr, 0, nullptr, nullptr);
    if (chars_num == 0) return "";

    // 3. Конвертируем из UTF-16 в UTF-8
    std::string result(chars_num, 0);
    WideCharToMultiByte(CP_UTF8, 0, wstr.c_str(), -1, &result[0], chars_num, nullptr, nullptr);

    return result;
}
static int callback(void* data, int argc, char** argv, char** azColName) {
    // data - это то, что мы передали в 4-м параметре sqlite3_exec (у нас это "Строки:")
    std::cout << ToUtf8((char*)data) << std::endl;

    for (int i = 0; i < argc; i++) {
        // Если значение не NULL, выводим его. Если NULL - выводим "NULL"
        std::cout <<ToUtf8(azColName[i]) << " = " << (argv[i] ? argv[i] : "NULL") << "\t";
    }
    std::cout << "\n----------------------\n";
    return 0;
}

int main() {
    SetConsoleCP(CP_UTF8);
    SetConsoleOutputCP(CP_UTF8);
    sqlite3* DB;
    int exit = 0;

    exit = sqlite3_open("fitness_club.db", &DB);

    if (exit) {
        // Используем ToUtf8 для сообщения об ошибке
        std::string err_msg = ToUtf8(sqlite3_errmsg(DB));
        std::cerr << err_msg << std::endl; // std::cerr теперь тоже работает с UTF-8 строками
        return(-1);
    }
    else {
        std::cout << ToUtf8("База данных успешно открыта!\n");
    }

    const char* sql = "SELECT name AS Имя, phone AS Телефон FROM clients LIMIT 5;";

    char* messageError;
    exit = sqlite3_exec(DB, sql, callback, (void*)"Список клиентов:", &messageError);

    if (exit != SQLITE_OK) {
        std::string err_msg = ToUtf8(messageError);
        std::cerr << err_msg << std::endl;
        sqlite3_free(messageError);
    }
    else {
        std::cout << ToUtf8("Запрос выполнен успешно\n");
    }

    sqlite3_close(DB);

    std::cout << ToUtf8("\nНажмите Enter для выхода...");
    std::cin.get();

    return 0;
}