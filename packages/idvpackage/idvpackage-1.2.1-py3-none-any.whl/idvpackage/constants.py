DATA_COMPARISON = {
      "breakdown": {
        "date_of_birth": {
          "properties": {}
        },
        "date_of_expiry": {
          "properties": {}
        },
        "document_numbers": {
          "properties": {}
        },
        "document_type": {
          "properties": {}
        },
        "first_name": {
          "properties": {}
        },
        "gender": {
          "properties": {}
        },
        "issuing_country": {
          "properties": {}
        },
        "last_name": {
          "properties": {}
        }
      }
    }

DATA_CONSISTENCY = {
      "breakdown": {
        "date_of_birth": {
          "properties": {},
          "result": "clear"
        },
        "date_of_expiry": {
          "properties": {},
          "result": "clear"
        },
        "document_numbers": {
          "properties": {},
          "result": "clear"
        },
        "document_type": {
          "properties": {},
          "result": "clear"
        },
        "first_name": {
          "properties": {},
          "result": "clear"
        },
        "gender": {
          "properties": {},
          "result": "clear"
        },
        "issuing_country": {
          "properties": {},
          "result": "clear"
        },
        "last_name": {
          "properties": {},
          "result": "clear"
        },
        "multiple_data_sources_present": {
          "properties": {},
          "result": "clear"
        },
        "nationality": {
          "properties": {},
          "result": "clear"
        }
      },
      "result": "clear"
    }

DATA_VALIDATION = {
    "breakdown": {
        "date_of_birth": {
            "properties": {},
            "result": "clear"
        },
        "document_expiration": {
            "properties": {},
            "result": "clear"
        },
        "document_numbers": {
            "properties": {},
            "result": "clear"
        },
        "expiry_date": {
            "properties": {},
            "result": "clear"
        },
        "gender": {
            "properties": {},
            "result": "clear"
        },
        "mrz": {
            "properties": {},
            "result": "clear"
        },
        "barcode": {
            "properties": {},
            "result": "clear"
        }
    },
    "result": "clear"
}

IMAGE_INTEGRITY = {
      "breakdown": {
        "colour_picture": {
          "properties": {},
          "result": "clear"
        },
        "conclusive_document_quality": {
          "properties": {
              "missing_back": "clear",
              "digital_document": "clear", ## digital or printed
              "punctured_document": "clear", ## EDC
              "corner_removed": "clear", 
              "watermarks_digital_text_overlay": "clear",
              "abnormal_document_features": "clear",
              "obscured_security_features": "clear",
              # TODO: integrate font rec
              "obscured_data_points": "clear" ## font recognition
            },
          "result": "clear"
        },
        "image_quality": {
          "properties": {
              "blurred_photo": "clear",
              "covered_photo": "clear",
              "cut_off_document": "clear",
              "glare_on_photo": "clear",
              "other_photo_issue": "clear",
              # TODO: pending, check for multiple docs
              "two_documents_uploaded": "clear"
          },
          "result": "clear"
        },
        "supported_document": {
          "properties": {},
          "result": "clear"
        }
      },
      "result": "clear"
    }

VISUAL_AUTHENTICITY = {
      "breakdown": {
        # TODO conclusive result - tamper detection
        "digital_tampering": {
          "properties": {},
          "result": "clear"
        },
        "face_detection": {
          "properties": {},
          "result": "clear"
        },
        # TODO font recognition - tamper detection
        "fonts": {
          "properties": {},
          "result": "clear"
        },
        "original_document_present": {
          "properties": {
                "scan": "clear",
                "document_on_printed_paper": "clear",
                "screenshot": "clear",
                "photo_of_screen": "clear"
          },
          "result": "clear"
        },
        "other": {
          "properties":  {},
          "result": "clear"
        },
        "picture_face_integrity": {
          "properties": {},
          "result": "clear"
        },
        "security_features": {
          "properties": {},
          "result": "clear"
        },
        # TODO - tamper detection
        "template": {
          "properties": {},
          "result": "clear"
        }
      },
      "result": "clear"
    }

MAIN_DATA = {
        ## barcode is empty in all instance - TBD
        'barcode': [],
        "date_of_birth": "",
        "date_of_expiry": "",
        "document_numbers": [],
        "document_type": "",
        "first_name": "",
        "gender": "",
        "issuing_country": "",
        "last_name": "",
        "mrz_line1": "",
        "mrz_line2": "",
        "mrz_line3": "",
        "nationality": ""
    }

FACIAL_REPORT = {
        "created_at": "",
        ## pending - to be filled by dev
        "href": "/v3.6/reports/<REPORT_ID>",
        ## pending - to be filled by dev
        "id": "<REPORT_ID>",
        "name": "facial_similarity_video",
        "properties": {},
        "breakdown": {
            "face_comparison": {
                "breakdown": {
                    "face_match": { 
                        "properties": {
                            "score": 0,
                            ## pending - to be filled by dev
                            "document_id": "<DOCUMENT_ID>"
                        },
                        "result": "clear", 
                    }
                },
                "result": "clear"
            },
            "image_integrity": {
                "breakdown": {
                    "face_detected": {
                        "result": "clear",
                        "properties": {}
                    },
                    ## pending
                    "source_integrity": {
                        "result": "clear",
                        "properties": {}
                    }
                },
                "result": "clear",
            },
            "visual_authenticity": {
                "breakdown": {
                    "liveness_detected": {
                        "properties": {},
                        "result": "clear",
                    },
                    "spoofing_detection": {
                        "properties": {
                            "score": 0.90
                        },
                        "result": "clear",
                    }
                },
                "result": "clear",
            }
        },
        "result": "clear",
        "status": "complete",
        "sub_result": "clear",
        ## pending - to be filled by dev
        "check_id": "<CHECK_ID>",
        "documents": []
        }

GOOGLE_MAPS_API_ENDPOINT = "https://maps.googleapis.com/maps/api/geocode/json"

API_KEY = "AIzaSyC3jF85Z6qgAEBwqwCdP8j_YM_XQcvEH-s"

