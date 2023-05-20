from garbage.session import Session

if __name__ == '__main__':

    session = Session.new()

    for idx in range (5):
        session.step()

    session.end()