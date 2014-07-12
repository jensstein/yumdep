PREFIX=/usr/local
SYSCONFDIR=/etc

install:
	mkdir -p $(PREFIX)/bin
	install -m 755 yumdep.py $(PREFIX)/bin/yumdep
	mkdir -p $(SYSCONFDIR)/bash_completion.d
	install -m 644 yumdep.bash $(SYSCONFDIR)/bash_completion.d/yumdep.bash

uninstall:
	rm $(PREFIX)/bin/yumdep
	rm $(SYSCONFDIR)/bash_completion.d/yumdep.bash
