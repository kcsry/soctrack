from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('medium', models.CharField(max_length=4, choices=[('ig', 'Instagram'), ('tw', 'Twitter')])),
                ('identifier', models.CharField(max_length=64)),
                ('downloaded_on', models.DateTimeField(auto_now_add=True)),
                ('posted_on', models.DateTimeField(db_index=True, null=True, blank=True)),
                ('hidden', models.BooleanField(default=False, db_index=True)),
                ('post_url', models.URLField(max_length=128, blank=True)),
                ('avatar_url', models.URLField(max_length=128, blank=True)),
                ('primary_image_url', models.URLField(max_length=128, blank=True)),
                ('author_name', models.CharField(max_length=64, blank=True)),
                ('message', models.CharField(max_length=140, blank=True)),
                ('blob', jsonfield.fields.JSONField()),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(max_length=64, db_index=True)),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='soctrack.Tag'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='post',
            unique_together={('medium', 'identifier')},
        ),
    ]
