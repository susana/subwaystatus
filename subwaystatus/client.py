from time import time
import json

import requests
from bs4 import BeautifulSoup


class Client(object):

    VALID_LINES = ["123", "456", "7", "ACE", "BDFM", "G", "JZ", "L", "NQR", "S", "SIR"]

    def __init__(self, path):
        self.path = path

    def get_status(self, lines=None):
        if lines is None:
            lines = self.VALID_LINES
        self._validate_lines(lines)
        response = self._get_status()
        return self._clean(response)

    def _validate_lines(self, requested_lines):
        """Compares lines in `requested_lines` against `VALID_LINES` and raises
           a ValueError if there were any were not found in `VALID_LINES`.

           Args:
               requested_lines (list): The subway lines requested.
        """
        requested_lines = [r.upper() for r in requested_lines]
        invalid_lines = [r for r in requested_lines if r not in self.VALID_LINES]

        if invalid_lines:
            invalid_lines_str = ", ".join(invalid_lines)
            valid_lines_str = ", ".join(self.VALID_LINES)
            raise ValueError("Invalid lines {}. Try {}.".format(
              invalid_lines_str,
              valid_lines_str))

    def _calc_diff(self):
        return int(round(time() * 1000 / 60000))

    def _get_status(self):
        """Returns Response object after making request to service status endpoint.

           Returns:
               Response object
        """
        diff = str(self._calc_diff())
        path = self.path + diff
        return requests.get(path)

    def _clean(self, response):
        """

           Args:
               response (Response): The response returned from _get_status
           Returns:
               A list of line statuses sorted by line name.
        """
        json_resp = json.loads(json.loads(response.text))
        line_statuses = json_resp.get("subway", {}).get("line", {})
        cleaned_statuses = []

        for line_status in line_statuses:
            if line_status:
                name = line_status.get("name", "").upper()
                status = line_status.get("status", "") if line_status.get("status") else ""
                text = line_status.get("text", "") if line_status.get("text") else ""
                # `text` contains HTML so we parse it and then strip out the HTML
                soup = BeautifulSoup(text, "html.parser")
                text = soup.get_text()
                text = text
                text = text.strip()
                cleaned_statuses.append({"line": name, "status": status, "text": text})

        return cleaned_statuses
