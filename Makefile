
# ╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                                                                                               ║
# ║                                                                                                               ║
# ║     ██████╗ █████╗ ██╗     ██╗         ███╗   ███╗███████╗    ███╗   ███╗ █████╗ ██╗   ██╗██████╗ ███████╗    ║
# ║    ██╔════╝██╔══██╗██║     ██║         ████╗ ████║██╔════╝    ████╗ ████║██╔══██╗╚██╗ ██╔╝██╔══██╗██╔════╝    ║
# ║    ██║     ███████║██║     ██║         ██╔████╔██║█████╗      ██╔████╔██║███████║ ╚████╔╝ ██████╔╝█████╗      ║
# ║    ██║     ██╔══██║██║     ██║         ██║╚██╔╝██║██╔══╝      ██║╚██╔╝██║██╔══██║  ╚██╔╝  ██╔══██╗██╔══╝      ║
# ║    ╚██████╗██║  ██║███████╗███████╗    ██║ ╚═╝ ██║███████╗    ██║ ╚═╝ ██║██║  ██║   ██║   ██████╔╝███████╗    ║
# ║     ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝    ╚═╝     ╚═╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚══════╝    ║
# ║                                                                                                               ║
# ║                                                                                                               ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

# Site for text : https://patorjk.com/software/taag/
# Site for box : https://onlinetexttools.com/draw-box-around-text

# ══════════════════ COLORS ══════════════════

GREEN	:= \033[1;32m
YELLOW	:= \033[1;33m
BLUE	:= \033[1;34m
PURPLE	:= \033[1;35m
CYAN	:= \033[1;36m
NC		:= \033[0m # No Color (Reinitialization)

# Github ASCII colors: https://gist.github.com/JBlond/2fea43a3049b38287e5e9cefc87b2124



# ══════════════════ HELP ══════════════════
.DEFAULT_GOAL := help

help:
	@printf "\n${BOLD}${PURPLE}>> CALL ME MAYBE'S MAKEFILE ${NC}\n\n"
	@printf "${CYAN}Usage:${NC} make <target>\n\n"
	@printf "${YELLOW}Available commands :${NC}\n"
	@printf "  ${GREEN}install${NC}       Create a virtual environement and install required dependencies\n"
	@printf "  ${GREEN}run${NC}           Run the main program (takes an ARG and an OPTION)\n"
	@printf "  ${GREEN}debug${NC}         Run the main file in debug mode\n"
	@printf "  ${GREEN}clean${NC}         Clean temporary files and caches\n"
	@printf "  ${GREEN}lint${NC}          Check project's norm (flake8 & mypy)\n"
	@printf "  ${GREEN}lint-strict${NC}   A strict norm check\n"



# ══════════════════ VARIABLES ══════════════════

UV			:= uv
PYTHON		:= python3
NAME		:= src
DEBUGGER	:= pdb
ARG			?=



# ══════════════════ RULES ══════════════════

install:
	@printf "${BLUE}{make} ==> Creating virtual environement and syncing packages...${NC}\n"
	@${UV} sync
	@printf "${YELLOW}{make} ==> Installation done.${NC}\n"

run:
	@printf "${BLUE}{make} ==> Running the main program...${NC}\n"
	${UV} run ${PYTHON} -m ${NAME} ${ARG}

debug:
	@printf "${CYAN}{make} ==> Running the main file in debug mode (using ${DEBUGGER})...${NC}\n"
	@${UV} run ${PYTHON} -m ${DEBUGGER} ${NAME} ${ARG}

clean:
	@find . -name "__pycache__" -type d -exec rm -rf {} +
	@find . -name ".mypy_cache" -type d -exec rm -rf {} +
	@find . -name ".venv" -type d -exec rm -rf {} +
	@printf "${PURPLE}{make} ==> Cleaned temporary virtual environement and caches${NC}\n"

lint:
	@printf "${YELLOW}{make} ==> Checking norm of the project...${NC}\n"
	@${PYTHON} -m flake8 .
	@mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	@printf "${GREEN}{make} ==> Norm checking done. Everything is fine :)${NC}\n"

lint-strict:
	@printf "${YELLOW}{make} ==> Checking strict norm of the project...${NC}\n"
	@${PYTHON} -m flake8 .
	@mypy . --strict
	@printf "${GREEN}{make} ==> Strict norm checking done. Everything is fine :)${NC}\n"


.PHONY: install run debug clean lint lint-strict