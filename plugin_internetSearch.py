import dmenu_extended
import sys

file_prefs = dmenu_extended.path_prefs + '/internetSearch.json'

class extension(dmenu_extended.dmenu):

    title = 'Szukaj w Internecie: '
    is_submenu = True


    def __init__(self):
        self.load_preferences()

    def create_default_providers(self):
        default = {
            'providers': [
                {
                    'title': 'Google',
                    'url': 'https://www.google.com/search?q='
                },
                {
                    'title': 'DuckDuckGo',
                    'url': 'https://duckduckgo.com/?q='
                },
                {
                    'title': 'Wikipedia PL',
                    'url': 'https://pl.wikipedia.org/wiki/Special:Search?search='
                },
                {
                    'title': 'Google obrazki',
                    'url': 'https://www.google.com/images?q='
                },
                {
                    'title': 'Arch User Repository (AUR)',
                    'url': 'https://aur.archlinux.org/packages/?O=0\&K='
                },
                {
                    'title': 'Github',
                    'url':  'https://github.com/search?q='
                }
            ],
            'default': 'Google'
        }
        self.save_json(file_prefs, default)


    def load_providers(self):
        providers = self.load_json(file_prefs)
        if providers == False:
            self.create_default_providers()
            providers = self.load_json(file_prefs)
        return providers


    def conduct_search(self, searchTerm, providerName=False):
        default = self.providers['default']
        primary = False
        fallback = False
        for provider in self.providers['providers']:
            if provider['title'] == default:
                fallback = provider['url'] + searchTerm
            elif provider['title'] == providerName:
                primary = provider['url'] + searchTerm

        if primary:
            self.open_url(primary)
        else:
            self.open_url(fallback)


    def run(self, inputText):

        self.providers = self.load_providers()

        if inputText != '':
            self.conduct_search(inputText)
        else:

            items = []
            for provider in self.providers['providers']:
                items.append(provider['title'])

            item_editPrefs = self.prefs['indicator_edit'] + ' Edytuj strony'

            items.append(item_editPrefs)

            provider = self.menu(items, prompt='Wybierz stronę:')

            if provider == item_editPrefs:
                self.open_file(file_prefs)
            elif provider == '':
                sys.exit()
            else:
                if provider not in items:
                    self.conduct_search(provider)
                else:
                    search = self.menu('', prompt='Wyszukaj')
                    if search == '':
                        sys.exit()
                    else:
                        self.conduct_search(search, provider)
