"""Defines the class for building the session id."""
from framework.core.conversion.jsonutils import SessionTranscript
from framework.core.xmlutils import XmlAttributes
from framework.core.xmlutils import XmlDataManipulator


class SessionIdBuilder(XmlDataManipulator):
    """Builds the session id."""

    def __init__(self, template_file: str, transcript: SessionTranscript,
                 output_file: str):
        """Create a new instance of the class.

        Parameters
        ----------
        template_file: str, required
            The path of the session template file.
        transcript: SessionTranscript, required
        output_file, str, required
            The path of the output XML file.
        """
        XmlDataManipulator.__init__(self, template_file)
        self.__transcript = transcript
        self.__output_file = output_file

    def build_session_id(self):
        """Build session id and save file."""
        xml_id = "ParlaMint-RO_{}-id{}".format(self.__transcript.session_date,
                                               self.__transcript.session_id)
        self.xml_root.set(XmlAttributes.xml_id, xml_id)
        self.save_changes(self.__output_file)
