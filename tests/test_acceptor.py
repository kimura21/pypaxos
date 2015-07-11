from unittest import TestCase, main

from paxos.core.acceptor import Acceptor
from paxos.net.history_channel import HistoryChannel
from paxos.net.message import Prepare, Promise, Accept, Nack, Accepted
from paxos.net.proposal import Proposal


class TestAcceptor(TestCase):
    def test_receive_prepare_with_higher_proposal(self):
        channel = HistoryChannel()
        role = Acceptor()

        role.receive(Prepare.create(proposal=Proposal('A', 1)), channel)
        role.receive(Prepare.create(proposal=Proposal('A', 2)), channel)

        self.assertEqual(len(channel.unicast_messages), 2)
        self.assertEqual(role.last_proposal, Proposal('A', 2))
        self.assertTrue(type(channel.unicast_messages[-1]) is Promise)

    def test_receive_prepare_with_lower_proposal(self):
        channel = HistoryChannel()
        role = Acceptor()

        role.receive(Prepare.create(proposal=Proposal('A', 2)), channel)
        role.receive(Prepare.create(proposal=Proposal('A', 1)), channel)

        self.assertEqual(len(channel.unicast_messages), 2)
        self.assertEqual(role.last_proposal, Proposal('A', 2))
        self.assertTrue(type(channel.unicast_messages[-1]) is Nack)

    def test_receive_accept(self):
        channel = HistoryChannel()
        role = Acceptor()

        role.receive(Accept.create(), channel)

        self.assertTrue(type(channel.broadcast_messages[0]) is Accepted)


if __name__ == "__main__":
    main()

