VERSION = $(shell cat VERSION)
NAME=image-configurations
TAGVER = $(shell cat VERSION | sed -e "s/\([0-9\.]*\).*/\1/")

ifeq ($(VERSION), $(TAGVER))
	TAG = $(TAGVER)
else
	TAG = "HEAD"
endif

all: 

tag:
	git tag -a $(VERSION) -m " $(VERSION)"
	git push --tags origin master

dist-bz2:
	git archive --format=tar --prefix=$(NAME)-$(TAGVER)/ $(TAG) | \
		bzip2  > $(NAME)-$(TAGVER).tar.bz2

dist-gz:
	git archive --format=tar --prefix=$(NAME)-$(TAGVER)/ $(TAG) | \
		gzip  > $(NAME)-$(TAGVER).tar.gz

changelog:
	python ./scripts/gitlog2changelog.py

repackage: dist
	osc branch -c Tizen:Base $(NAME)
	rm home\:*\:branches\:Tizen:Base/$(NAME)/*tar.bz2
	cp $(NAME)-$(VERSION).tar.bz2 home\:*\:branches\:Tizen:Base/$(NAME)

dist: dist-bz2

install: all install-data

up:
	@python scripts/gitlog2changelog.py
	@echo 'Current versions:'
	@git tag -l
	@echo 'Please specify the new version:'
	@read NEWVER; echo $$NEWVER > VERSION; \
	git commit -a -m "bump version to $$NEWVER"; \
	git tag -m $$NEWVER $$NEWVER

clean:
