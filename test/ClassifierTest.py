from newsclassifier import RCV1NewsClassifi as NC
from newsclassifier.RCV1NewsClassifi import predict
from sklearn.datasets import fetch_rcv1

from utils.Paths import Paths

if __name__ == '__main__':
    NC.train()
    # text = 'A boat that symbolises hard work. An empty bowl that stands out ' \
    #        'among bowls filled with food. An installation which invites viewers ' \
    #        'to focus on the bright spots.These are among 81 pieces of artwork by ' \
    #        'inmates and former offenders on display at the Singapore Art Museum at the ninth ' \
    #        'Yellow Ribbon Community Art Exhibition, which is on from today till Sept 4.' \
    #        'For the art show, 42 inmates from Changi Prison Complex and Changi Women''s Prison created canvas paintings, ceramics and batik paintings. "Prison and art seem to be two different entities. But when you put them together, you see that in this exhibition, each artwork has a very powerful story - certain desires to be accepted back into their families and society at large," said superintendent of prisons Edwin Goh, 39.This year''s theme, From Night To Light, is about the emotional journey inmates go through before getting forgiveness and acceptance.The exhibition''s artist-in-residence Barry Yeow, 49, said his feature artwork and wall installation "Whole Again" is about the need to focus on the positive. Mr Yeow, who picked up art in prison and now runs his own art gallery, said the work signifies that "as inmates, even as we try to change, our dark past remains very real. We need to focus on the light, the beautiful colours, the beautiful people who have extended help and support to go on this journey with us".At the launch of the show yesterday evening, Minister for Culture, Community and Youth Grace Fu said: "(Art) contributes towards preventing ex-offenders from entering into a second societal prison of suspicion, mistrust and discrimination. It gives us the space and confidence to think beyond the constraints of our circumstances."Entry to the show is free for Singaporeans and permanent residents.'
    # predict(text)

