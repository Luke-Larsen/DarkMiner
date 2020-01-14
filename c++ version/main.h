#pragma once
#pragma comment (lib, "urlmon.lib") 
#pragma comment (lib, "wininet.lib")
#define INFO_BUFFER_SIZE 32767
#define WINDOWS_LEAN_AND_MEAN
#define _WINSOCK_DEPRECATED_NO_WARNINGS
#include <windows.h>
#include <wininet.h>
#include <fstream>
#include <map>
#include <chrono>
#include <future>
#include <ctime>
#include <iostream>
#include <string>
#pragma comment(lib,"ws2_32.lib")
#include <WinInet.h>
#include <sstream>
#include <tchar.h>
#include <urlmon.h>
#ifdef _UNICODE
#define tcout wcout
#else
#define tcout cout
#endif



