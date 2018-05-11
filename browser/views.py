from django.shortcuts import render
# Create your views here.
from django.views import generic
from .models import Request, ComponentSpecification
from .filters import ComponentFilter
from django_filters.views import FilterView


class ComponentDetailView(generic.DetailView):
    model = ComponentSpecification
    template_name = 'browser/component_detail.html'


class RequestDetailView(generic.DetailView):
    model = Request
    template_name = 'browser/request_detail.html'

    def get_context_data(self, **kwargs):

        context = {'request': {k: v for k, v in self.object.__dict__.items() if k != '_state'}}

        def extract_fields(dictionary):

            parameters = {}

            for k, v in dictionary.items():
                k = k if k != 'enum' else 'options'

                if k not in ['_state', 'id'] and v is not None:
                    parameters[k] = v

            return parameters

        def extract_parameters(objects, is_nested=False):

            internal_parameters = []

            for obj in objects:

                nested_params = obj.nested.all()
                if nested_params:
                    nested_params = extract_parameters(nested_params, True)

                param_dict = obj.__dict__
                if nested_params:
                    param_dict['nested'] = nested_params

                internal_parameters.append(extract_fields(param_dict))

            return internal_parameters

        context['parameters'] = extract_parameters(self.object.parameters.filter(sub_param=None))

        return context


# from django.views import generic
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#
# class ComponentGridView(generic.ListView):
#     model = Question
#     template_name = 'your_app_name/questions.html'
#     context_object_name = 'questions'
#     paginate_by = 10
#     queryset = Question.objects.all()


# def search(request):
#     component_list = ComponentSpecification.objects.all()
#     component_filter = ComponentFilter(request.GET, queryset=component_list)
#     return render(request, 'search/user_list.html', {'filter': component_filter})


class ComponentFilterView(FilterView):
    filterset_class = ComponentFilter
    template_name = 'browser/index.html'
    paginate_by = 4


# class IndexView(generic.ListView):
#     template_name = 'browser/index.html'
#     context_object_name = 'component_specifications'
#     model = ComponentSpecification
#     paginate_by = 3
#
#     user_filter = ComponentFilter(self.request.GET, queryset=user_list)
#
#     def get_queryset(self):
#
#
#
#         return ComponentSpecification.objects.prefetch_related('request_set').all()
