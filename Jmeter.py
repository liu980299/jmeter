from django.template import Template,Context

class JMXClass(object):
   def __init__(self, template):
      self.template = template
      self.data ={}
      self.children = []
      self.childrentemplate = []

   def render(self):
      data = {}
      attrs = dir(self)
      for attr in attrs:
         instance = getattr(self,attr)
         if isinstance(instance,JMXClass):
            data[attr]=instance.render()
      data['children']=[]
      for child in self.children:
         if isinstance(child,JMXClass):
            data['children'].append(child.render())
      return Template(self.template).render(Context(self.data))

class JMXPlan(JMXClass):
   template = '''
   <?xml version="1.0" encoding="UTF-8"?>
   <jmeterTestPlan version="1.2" properties="2.8" jmeter="2.13 r1665067">
     <hashTree>
      <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="{{name}}" enabled="true">
        <stringProp name="TestPlan.comments">{{comments}}</stringProp>
        <boolProp name="TestPlan.functional_mode">{{functional_mode}}</boolProp>
        <boolProp name="TestPlan.serialize_threadgroups">{{serialize_threadgroups}}</boolProp>
        <elementProp name="TestPlan.user_defined_variables" elementType="Arguments" guiclass="ArgumentsPanel" testclass="Arguments" testname="User Defined Variables" enabled="true">
        {{arguments}}
        </elementProp>
        <stringProp name="TestPlan.user_define_classpath"></stringProp>
      </TestPlan>
      <hashTree>
      </hashTree>
     </hashTree>
   </jmeterTestPlan>
   '''
   def __init__(self, name, comments='',functional_mode='false', serialize_threadgroups='false'):
      self.name = name
      self.comments=comments
      self.functional_mode = functional_mode
      self.serialize_threadgroups = serialize_threadgroups
      self.thread_groups = []

class JMXArguments(JMXClass):
   template='''
   <collectionProp name="Arguments.arguments">
   {% for child in children %}
      {{child}}
   {% endfor %}
   </collectionProp>
   '''
   def __init__(self, arguments):
      self.arguments = arguments

class JMXArgument(JMXClass):
   tempalte='''
     <elementProp name="{{name}}" elementType="Argument">
      <stringProp name="Argument.name">{{name}}</stringProp>
      <stringProp name="Argument.value">{{value}}</stringProp>
      <stringProp name="Argument.metadata">=</stringProp>
     </elementProp>
   '''

   def __init__(self,name,value):
      self.name = name
      self.value = value

class JMXThreadgroup(JMXClass):
   template='''
      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="Thread Group" enabled="true">
        <stringProp name="ThreadGroup.on_sample_error">{{errorProcess}}</stringProp>
        <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" testclass="LoopController" testname="Loop Controller" enabled="true">
          <boolProp name="LoopController.continue_forever">{{forEver}}</boolProp>
          <stringProp name="LoopController.loops">{{loops}}</stringProp>
        </elementProp>
        <stringProp name="ThreadGroup.num_threads">{{threads}}</stringProp>
        <stringProp name="ThreadGroup.ramp_time">{{ramp_time}}</stringProp>
        <longProp name="ThreadGroup.start_time">{{start_time}}</longProp>
        <longProp name="ThreadGroup.end_time">{{end_time}}</longProp>
        <boolProp name="ThreadGroup.scheduler">{{isScheduler}}</boolProp>
        <stringProp name="ThreadGroup.duration">{{duration}}</stringProp>
        <stringProp name="ThreadGroup.delay">{{delay}}</stringProp>
      </ThreadGroup>
      <hashTree>
      {% for child in children %}
       {{child}}
      {% endfor %}
      </hashTree>
   '''
   def __init__(self,errorProcess,):
       pass