import operator

def sortBookList(bookList, sortBy='relevance'):
    if(sortBy=='relevance'):
        return bookList
    else:
        return sorted(bookList, key=operator.attrgetter(sortBy))

class Book:
    def __init__(self, bookData):
        self.title = bookData['volumeInfo']['title']
        self.authors = bookData['volumeInfo']['authors']
        self.imageLink = bookData['volumeInfo']['imageLinks']['smallThumbnail']
        self.description = bookData['volumeInfo']['description']

