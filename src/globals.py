from typing import Final, Sequence

from callbacks.Feedback import Feedback
from callbacks.SimpleFeedback import SimpleFeedback
from callbacks.RotatingFeedback import RotatingFeedBack
from callbacks.MultivoiceFeedback import MultivoiceFeedback

FEEDBACK_ARR:Final[Sequence[type[Feedback]]] = [SimpleFeedback, RotatingFeedBack, MultivoiceFeedback] # Array of classes
