import operator

def sortBookList(bookList, sortBy='relevance'):
    if(sortBy=='relevance'):
        return bookList
    else:
        return sorted(bookList, key=operator.attrgetter(sortBy))

class Book:
    def __init__(self, bookData):
        self.title = bookData['volumeInfo']['title']
        self.authors = bookData['volumeInfo']['authors'][0]
        for i in range(1, len(bookData['volumeInfo']['authors'])):
            self.authors = self.authors + ", " + bookData['volumeInfo']['authors'][i]
        self.imageLink = bookData['volumeInfo']['imageLinks']['smallThumbnail']
        self.description = bookData['volumeInfo']['description']
        self.id = bookData['id']

