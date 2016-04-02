from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import View

from actstream.models import model_stream
from git import Repo
from git.exc import NoSuchPathError
from datetime import datetime


class Index(View):
    template_name = 'bp_cupid/index.html'

    @method_decorator(login_required)
    def get(self, request):
        if request.user.is_staff:
            context = dict()

            # alle Aktivitäten die von Users kommen:
            action_stream = model_stream(request.user)[:15]
            context['action_stream'] = action_stream

            # die letzten 15 Commits aus dem git-Repo:
            try:
                repo = Repo(settings.GIT_DIR)
                commits = list(
                    filter(
                        # filtere alle Mergecommits heraus:
                        lambda c: not c.summary.startswith('Merge'),
                        repo.iter_commits()
                    )
                )[:15]
                last_commits = []

                for commit in commits:
                    c = dict()
                    c['date'] = datetime.fromtimestamp(commit.committed_date)
                    c['summary'] = commit.summary
                    last_commits.append(c)
                context['commits'] = last_commits
            except NoSuchPathError:
                pass
            except AttributeError:
                pass

            return render(request, self.template_name, context)
        else:
            return redirect('bp_setup:index')
