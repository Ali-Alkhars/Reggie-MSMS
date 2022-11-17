from django import forms


weekday_choices = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
]

time_choices = [
    ('Morning', 'Morning'),
    ('Afternoon', 'Afternoon'),
    ('Night', 'Night'),
]

# Request form for the lesson
class LessonRequestForm(forms.Form):
    avaiableDays = forms.CharField(label="Available days: ", widget=forms.Select(choices=weekday_choices), blank=False)
    availableTimes = forms.CharField(label="Available times: ", widget=forms.Select(choices=time_choices), blank=False)
    numberOfLessons = forms.IntegerField(label="Number of lessons desired: ", blank=False);
    IntervalBetweenLessons = forms.IntegerField(label="Interval between lessons (In weeks): ", blank=False);
    DurationOfLesson = forms.DecimalField(label="Duration of lesson (In minutes): ", blank = False);
    LearningObjectives = forms.CharField(widget=forms.Textarea);
    AdditionalNotes = forms.CharField(widget=forms.Textarea);





