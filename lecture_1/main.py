from colorama import Back, Fore, Style, init

init()

print(f"{Fore.RED}{Back.YELLOW}Hello World!{Style.RESET_ALL}")
print(f"{Fore.GREEN}Hello World in Green!{Style.RESET_ALL}")
print(f"{Fore.BLUE}{Style.BRIGHT}Hello World in Blue!{Style.RESET_ALL}")
print(
    f"{Fore.MAGENTA}{Back.CYAN}Hello World with Magenta Cyan Background!{Style.RESET_ALL}"
)
