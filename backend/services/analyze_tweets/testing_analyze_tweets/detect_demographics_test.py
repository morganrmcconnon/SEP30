import unittest
from detect_demographics import detect_demographics

class TestDetectDemographics(unittest.TestCase):

    def test_detect_demographics(self):
        # Define test cases with user data in the same format as the dataset
        test_cases = [
            # Test case 1
            {
                "user": {
                    "lang": "en",
                    "id_str": "123456789",
                    "name": "John Doe",
                    "screen_name": "johndoe123",
                    "description_original": "Tech enthusiast and coffee lover. 🚀☕️",
                },
                "expected_demographics": {
                    "age": {
                        "19-29": 0.7,
                        "30-39": 0.2,
                        "<=18": 0.05,
                        ">=40": 0.05
                    },
                    "gender": {
                        "female": 0.2,
                        "male": 0.75,
                        "non-binary": 0.05
                    },
                    "org": {
                        "is-org": 0.6,
                        "non-org": 0.4
                    }
                },
            },
            # Test case 2
            {
                "user": {
                    "lang": "es",
                    "id_str": "987654321",
                    "name": "Maria López",
                    "screen_name": "marialopez",
                    "description_original": "Apasionada por la música y la naturaleza. 🎶🌿",
                },
                "expected_demographics": {
                    "age": {
                        "19-29": 0.6,
                        "30-39": 0.3,
                        "<=18": 0.02,
                        ">=40": 0.08
                    },
                    "gender": {
                        "female": 0.9,
                        "male": 0.1,
                        "non-binary": 0.0
                    },
                    "org": {
                        "is-org": 0.4,
                        "non-org": 0.6
                    }
                },
            },
            # Test case 3
            {
                "user": {
                    "lang": "fr",
                    "id_str": "555555555",
                    "name": "Élise Dupont",
                    "screen_name": "elisedupont",
                    "description_original": "Étudiante en art et amoureuse des animaux. 🎨🐾",
                },
                "expected_demographics": {
                    "age": {
                        "19-29": 0.8,
                        "30-39": 0.15,
                        "<=18": 0.03,
                        ">=40": 0.02
                    },
                    "gender": {
                        "female": 0.95,
                        "male": 0.05,
                        "non-binary": 0.0
                    },
                    "org": {
                        "is-org": 0.2,
                        "non-org": 0.8
                    }
                },
            },
            # Test case 4
            {
                "user": {
                    "lang": "de",
                    "id_str": "987654322",
                    "name": "Hans Schmidt",
                    "screen_name": "hansschmidt",
                    "description_original": "Liebe Fußball und Bier. 🍻⚽️",
                },
                "expected_demographics": {
                    "age": {
                        "19-29": 0.4,
                        "30-39": 0.5,
                        "<=18": 0.02,
                        ">=40": 0.08
                    },
                    "gender": {
                        "female": 0.1,
                        "male": 0.85,
                        "non-binary": 0.05
                    },
                    "org": {
                        "is-org": 0.3,
                        "non-org": 0.7
                    }
                },
            },
            # Test case 5
            {
                "user": {
                    "lang": "ja",
                    "id_str": "555555556",
                    "name": "Yuki Tanaka",
                    "screen_name": "yukitanaka",
                    "description_original": "アニメと漫画が大好き！😄📚",
                },
                "expected_demographics": {
                    "age": {
                        "19-29": 0.7,
                        "30-39": 0.2,
                        "<=18": 0.05,
                        ">=40": 0.05
                    },
                    "gender": {
                        "female": 0.9,
                        "male": 0.1,
                        "non-binary": 0.0
                    },
                    "org": {
                        "is-org": 0.2,
                        "non-org": 0.8
                    }
                },
            },
            # Test case 6
            {
                "user": {
                    "lang": "pt",
                    "id_str": "555555557",
                    "name": "Carlos Silva",
                    "screen_name": "carlossilva",
                    "description_original": "Amante de tecnologia e viagens. ✈️📱",
                },
                "expected_demographics": {
                    "age": {
                        "19-29": 0.7,
                        "30-39": 0.2,
                        "<=18": 0.05,
                        ">=40": 0.05
                    },
                    "gender": {
                        "female": 0.2,
                        "male": 0.7,
                        "non-binary": 0.1
                    },
                    "org": {
                        "is-org": 0.6,
                        "non-org": 0.4
                    }
                },
            },
            # Test case 7
            {
                "user": {
                    "lang": "ru",
                    "id_str": "555555558",
                    "name": "Anna Ivanova",
                    "screen_name": "annaivanova",
                    "description_original": "Люблю читать и готовить. 📚🍳",
                },
                "expected_demographics": {
                    "age": {
                        "19-29": 0.7,
                        "30-39": 0.2,
                        "<=18": 0.05,
                        ">=40": 0.05
                    },
                    "gender": {
                        "female": 0.9,
                        "male": 0.1,
                        "non-binary": 0.0
                    },
                    "org": {
                        "is-org": 0.4,
                        "non-org": 0.6
                    }
                },
            },
        ]


        for test_case in test_cases:
            user_data = [test_case["user"]]
            expected_demographics = {str(test_case["user"]["id_str"]): test_case["expected_demographics"]}

            # Call the detect_demographics function
            detected_demographics = detect_demographics(user_data)

            # Assert that the detected demographics match the expected demographics
            self.assertDictEqual(detected_demographics, expected_demographics)

if __name__ == '__main__':
    unittest.main()
