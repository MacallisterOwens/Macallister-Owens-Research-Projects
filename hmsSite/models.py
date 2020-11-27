from django.db import models
from django.core.validators import RegexValidator
from django.core.files.base import ContentFile
from datetime import date
from copy import copy
from PIL import Image 
from io import BytesIO
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.html import mark_safe

# Create your models here.


# This will hold the schools/departments that you can put projects under
# the search drop down will change based on what there is
class School(models.Model):
    name = models.CharField("school/centre", max_length=150, blank=False, null=True)

    # an actual default will be included later on
    def __str__(self):
        return self.name

class Faculty(models.Model):
    name = models.CharField("faculty", max_length=150, blank=False, null=True)

    class Meta:
        verbose_name = "Faculty"
        verbose_name_plural = "Faculties"

    def __str__(self):
        return self.name

class Image_Stock(models.Model):
    name = models.CharField("image_stock_name", max_length=150, blank=True, null=True)
    image = models.ImageField("stock_image_no_upload", upload_to='images/', height_field=None, width_field=None, max_length=None, null=True)
    image_thumbnail = models.ImageField("stock image thumbnail", upload_to='thumbnails/', blank=True, null=True)

    class Meta:
        verbose_name = "Stock Image"
        verbose_name_plural = "Stock Images"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        filename = "%s.jpg" % self.image.name.split('.')[0]
        image = Image.open(self.image)
        # for PNG images discarding the alpha channel and fill it with some color
        if image.mode in ('RGBA', 'LA'):
            background = Image.new(image.mode[:-1], image.size, '#fff')
            background.paste(image, image.split()[-1])
            image = background
        ratio = image.width/image.height
        # this can be easily changed to whatever is best
        image = image.resize((int(ratio*1024), 1024))
        image_io = BytesIO()
        image.save(image_io, format='JPEG', quality=100)
        self.image.save(filename, ContentFile(image_io.getvalue()), save=False)
        
        p_thumbnail = copy(image)
        # this can be easily change to whatever is best
        p_thumbnail.thumbnail((256,256))
        p_thumbnail_io = BytesIO()
        p_thumbnail.save(p_thumbnail_io, format='JPEG', quality=100)
        self.image_thumbnail.save("%s_thumbnail.jpg" % self.image.name.split('.')[0], ContentFile(p_thumbnail_io.getvalue()), save=False)
        
        super(Image_Stock, self).save(*args, **kwargs)




# Holds all the information thats contained in a project page and everything else needed
# this maybe needs a way to be changed by the super admins if they want to change the field
# since he did briefly say that, to do this we will have to swap to nosql im pretty sure
class Project(models.Model):
    approved = models.BooleanField("project approved", default=False, blank=True)
    title = models.CharField("project title", max_length=300, blank=False, null=False)
    desc = models.TextField("project description", blank=False, null=False)
    short_desc = models.CharField("project short description ~30 words", max_length=300, blank=False, null=True)
    readings = models.TextField("suggested readings", blank=True, null=True)
    goals = models.TextField("project goals", blank=True, null=True)
    collab = models.TextField("collaborations", blank=True, null=True)
    funds = models.TextField("project funding", blank=True, null=True)
    benefits = models.TextField("applicant benefits", blank=True, null=True)
    scholarships = models.TextField("scholarships fundings", blank=True, null=True)
    other = models.TextField("other information", blank=True, null=True)
    qualifications = models.TextField("applicant mandatory qualifications", blank=False, null=False)
    pref_qualifications = models.TextField("additional preferred qualifications", blank=True, null=False)

    start_date = models.DateField("project start date", blank=False, null=False, default=date.today)
    end_date = models.DateField("project end date", blank=False, null=False, default=date.today)
    
    phone_regex = RegexValidator(regex=r'\+?\d{9,15}', message="Invalid phone number.")

    contact1_name = models.CharField("primary contact name", max_length=150, blank=False, null=True)
    contact1_url = models.URLField("research repository URL", blank=False, null=True)
    contact1_email = models.EmailField("primary contact email", blank=False, null=True)
    contact1_phone = models.CharField("primary phone number",validators=[phone_regex], max_length=16, blank=True, null=True)

    contact2_name = models.CharField("seconday contact name", max_length=150, blank=True, null=True)
    contact2_url = models.URLField("research repository URL", blank=True, null=True)
    contact2_email = models.EmailField("secondary contact email", blank=True, null=True)
    contact2_phone = models.CharField("secondary phone number",validators=[phone_regex], max_length=16, blank=True, null=True)
    
    last_reminder = models.DateField("date of the previous archive reminder", blank=False, null=False, default=date.today)
    email_sent = models.BooleanField("is the project still relevant and ongoing", default=False, blank=False)

    # references to the other models, many to one relationship
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, blank=False, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    
    image = models.ImageField("image displayed on page", upload_to='images/',  blank=True, null=True)
    image_thumbnail = models.ImageField("thumbnail displayed on page", upload_to='thumbnails/', blank=True, null=True)
    image_stock = models.ForeignKey(Image_Stock, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

    # when an image is uploaded convert to jpg, resize to be standard size, create a thumbnail
    def save_form(self, *args, **kwargs):
        if self.image:
            filename = "%s.jpg" % self.image.name.split('.')[0]
            image = Image.open(self.image)
            # for PNG images discarding the alpha channel and fill it with some color
            if image.mode in ('RGBA', 'LA'):
                background = Image.new(image.mode[:-1], image.size, '#fff')
                background.paste(image, image.split()[-1])
                image = background
            ratio = image.width/image.height
            # this can be easily changed to whatever is best
            image = image.resize((int(ratio*1024), 1024))
            image_io = BytesIO()
            image.save(image_io, format='JPEG', quality=100)
            self.image.save(filename, ContentFile(image_io.getvalue()), save=False)
            
            p_thumbnail = copy(image)
            # this can be easily change to whatever is best
            p_thumbnail.thumbnail((256,256))
            p_thumbnail_io = BytesIO()
            p_thumbnail.save(p_thumbnail_io, format='JPEG', quality=100)
            self.image_thumbnail.save("%s_thumbnail.jpg" % self.image.name.split('.')[0], ContentFile(p_thumbnail_io.getvalue()), save=False)

        # if image is not uploaded but the selection is passed then the image field will point to the selected image path

        super(Project, self).save(*args, **kwargs)

    def archive(self):
        archive = ArchivedProject(approved=self.approved, title=self.title, desc=self.desc, short_desc=self.short_desc, 
            readings=self.readings, goals=self.goals, collab=self.collab, funds=self.funds, benefits=self.benefits, 
            scholarships=self.scholarships, other=self.other, qualifications=self.qualifications, 
            pref_qualifications=self.pref_qualifications, start_date=self.start_date, end_date=self.end_date, 
            contact1_name=self.contact1_name, contact1_url=self.contact1_url, contact1_email=self.contact1_email, 
            contact1_phone=self.contact1_phone, contact2_name=self.contact2_name, contact2_url=self.contact2_url, 
            contact2_email=self.contact2_email, contact2_phone=self.contact2_phone, faculty=self.faculty, school=self.school,
            user=self.user, image=self.image, image_thumbnail=self.image_thumbnail)
        archive.save()
        self.user.email_user(
            f'Your project - {self.title} - has been archived',
            f'Hello {self.user.get_full_name()},\r\n\r\nYour project - {self.title} - has been archived.\r\n\r\nThis is an automated email. Please do not reply to it.',
            ''
        )
        self.delete();

class ArchivedProject(models.Model):
    class Meta:
        verbose_name = "Archived Project"
        verbose_name_plural = "Archived Projects"

    approved = models.BooleanField("project approved", default=False, blank=True)
    title = models.CharField("project title", max_length=300, blank=False, null=False)
    desc = models.TextField("project description", blank=False, null=False)
    short_desc = models.CharField("project short description ~30 words", max_length=300, blank=False, null=True)
    readings = models.TextField("suggested readings", blank=True, null=True)
    goals = models.TextField("project goals", blank=True, null=True)
    collab = models.TextField("collaborations", blank=True, null=True)
    funds = models.TextField("project funding", blank=True, null=True)
    benefits = models.TextField("applicant benefits", blank=True, null=True)
    scholarships = models.TextField("scholarships fundings", blank=True, null=True)
    other = models.TextField("other information", blank=True, null=True)
    qualifications = models.TextField("applicant mandatory qualifications", blank=False, null=False)
    pref_qualifications = models.TextField("additional preferred qualifications", blank=True, null=False)

    start_date = models.DateField("project start date", blank=False, null=False, default=date.today)
    end_date = models.DateField("project end date", blank=False, null=False, default=date.today)
    
    contact1_name = models.CharField("primary contact name", max_length=150, blank=False, null=True)
    contact1_url = models.URLField("<a href=\"https://research-repository.uwa.edu.au/\" target=\"_blank\">Research Repositry URL<a/>", blank=False, null=True)
    contact1_email = models.EmailField("primary contact email", blank=False, null=True)
    contact1_phone = models.CharField("primary phone number", max_length=16, blank=True, null=True)

    contact2_name = models.CharField("seconday contact name", max_length=150, blank=True, null=True)
    contact2_url = models.URLField("<div class= \"url2\"> <a href=\"https://research-repository.uwa.edu.au/\" target=\"_blank\">Research Repositry URL<a/></div>", blank=True, null=True)
    contact2_email = models.EmailField("secondary contact email", blank=True, null=True)
    contact2_phone = models.CharField("secondary phone number", max_length=16, blank=True, null=True)
    
    # references to the other models, many to one relationship
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, blank=False, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    
    image = models.ImageField("image displayed on page", upload_to='images/',  blank=True, null=True)
    image_thumbnail = models.ImageField("thumbnail displayed on page", upload_to='thumbnails/', blank=True, null=True)

    def __str__(self):
        return self.title

    # when an image is uploaded convert to jpg, resize to be standard size, create a thumbnail
    def save_form(self, *args, **kwargs):
        if self.image:
            filename = "%s.jpg" % self.image.name.split('.')[0]
            image = Image.open(self.image)
            # for PNG images discarding the alpha channel and fill it with some color
            if image.mode in ('RGBA', 'LA'):
                background = Image.new(image.mode[:-1], image.size, '#fff')
                background.paste(image, image.split()[-1])
                image = background
            ratio = image.width/image.height
            # this can be easily changed to whatever is best
            image = image.resize((int(ratio*1024), 1024))
            image_io = BytesIO()
            image.save(image_io, format='JPEG', quality=100)
            self.image.save(filename, ContentFile(image_io.getvalue()), save=False)
            
            p_thumbnail = copy(image)
            # this can be easily change to whatever is best
            p_thumbnail.thumbnail((256,256))
            p_thumbnail_io = BytesIO()
            p_thumbnail.save(p_thumbnail_io, format='JPEG', quality=100)
            self.image_thumbnail.save("%s_thumbnail.jpg" % self.image.name.split('.')[0], ContentFile(p_thumbnail_io.getvalue()), save=False)

        super(ArchivedProject, self).save(*args, **kwargs)


    def archive(self):
        unarchive = Project(approved=self.approved, title=self.title, desc=self.desc, short_desc=self.short_desc, 
            readings=self.readings, goals=self.goals, collab=self.collab, funds=self.funds, benefits=self.benefits, 
            scholarships=self.scholarships, other=self.other, qualifications=self.qualifications, 
            pref_qualifications=self.pref_qualifications, start_date=self.start_date, end_date=self.end_date, 
            contact1_name=self.contact1_name, contact1_url=self.contact1_url, contact1_email=self.contact1_email, 
            contact1_phone=self.contact1_phone, contact2_name=self.contact2_name, contact2_url=self.contact2_url, 
            contact2_email=self.contact2_email, contact2_phone=self.contact2_phone, faculty=self.faculty, school=self.school,
            user=self.user, image=self.image, image_thumbnail=self.image_thumbnail)
        unarchive.save()
        self.delete();