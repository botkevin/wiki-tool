from mwclient import Site
import mwclient

class website_connection:
    ua = "MultiWikiTool run by User: "

    #params website_url, user, password
    def __init__(self, user, password, wikipath, page_name):
        self.website = Site(('http', 'wafwikifarm.hgst.com'), path=wikipath+'/', clients_useragent=self.ua + user)
        try:
            self.website.login(user, password)
        except mwclient.errors.LoginError:
            print("Incorrect login info")
            raise IOError('Incorrect login info for' + wikipath)
            #throw and catch error in parent block
        self.page = self.website.pages[page_name]

    #gets the text in the page, returns empty string if page does not exist
    def get_text(self):
        return self.page.text()

    def save_text(self, text, edit_summary):
        self.page.save(text, edit_summary)
