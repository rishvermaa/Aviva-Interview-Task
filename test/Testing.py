import unittest
import re
import uuid

#Function for extracting words that are 5+ letters
def find_words(text):
    return re.findall(r'\b\w{5,}\b', text.lower())

class TestPetitionProcessing(unittest.TestCase):
    
    def test_extract_words(self):
        #Testing the word extraction function.
        text = "We need atleast 50'%' of Health visitors & Midwifes to be funded to do the UNICEF babyfriendly initative training."
        words = find_words(text)
        self.assertEqual(words,['atleast', 'health', 'visitors', 'midwifes', 'funded', 'unicef', 'babyfriendly', 'initative', 'training'],'Word extraction failed!')

    def test_uuid_generation(self):
        #Testing unique IDs for petitions.
        uid = str(uuid.uuid4())[:8]
        self.assertEqual(len(uid), 8, "UUID is not the correct length!")
        self.assertIsInstance(uid, str, "UUID is not a string!")

if __name__ == '__main__':
    unittest.main()
