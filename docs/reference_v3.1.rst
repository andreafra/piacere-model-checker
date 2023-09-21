DOML v3.1 Reference
=============================


commons
^^^^^^^

.. _v3.1_commons_BProperty:

BProperty
"""""""""
*Inherits from* :ref:`Property <v3.1_commons_Property>`

* Attributes:
	* ``value`` [Boolean]

.. _v3.1_commons_Configuration:

Configuration
"""""""""""""
*Inherits from* :ref:`DOMLElement <v3.1_commons_DOMLElement>`

* Associations:
	* ``deployments`` → Deployment [0..*]

.. _v3.1_commons_Credentials:

Credentials
"""""""""""
*Inherits from* :ref:`DOMLElement <v3.1_commons_DOMLElement>`


.. _v3.1_commons_DOMLElement:

DOMLElement
"""""""""""
* Associations:
	* ``annotations`` → Property [0..*]
* Attributes:
	* ``name`` [String]
	* ``description`` [String]

.. _v3.1_commons_DeployableElement:

DeployableElement
"""""""""""""""""
*Inherits from* :ref:`DOMLElement <v3.1_commons_DOMLElement>`


.. _v3.1_commons_Deployment:

Deployment
""""""""""
* Associations:
	* ``component`` → DeployableElement [1..1]
	* ``node`` → InfrastructureElement [1..1]

.. _v3.1_commons_FProperty:

FProperty
"""""""""
*Inherits from* :ref:`Property <v3.1_commons_Property>`

* Attributes:
	* ``value`` [String]

.. _v3.1_commons_IProperty:

IProperty
"""""""""
*Inherits from* :ref:`Property <v3.1_commons_Property>`

* Attributes:
	* ``value`` [Integer]

.. _v3.1_commons_KeyPair:

KeyPair
"""""""
*Inherits from* :ref:`Credentials <v3.1_commons_Credentials>`

* Attributes:
	* ``user`` [String]
	* ``key`` [String]
	* ``algorithm`` [String]
	* ``bits`` [Integer]

.. _v3.1_commons_ListProperty:

ListProperty
""""""""""""
*Inherits from* :ref:`Property <v3.1_commons_Property>`

* Associations:
	* ``values`` → Property [0..*]

.. _v3.1_commons_Property:

Property
""""""""
* Associations:
	* ``reference`` → DOMLElement [0..1]
* Attributes:
	* ``key`` [String]

.. _v3.1_commons_SProperty:

SProperty
"""""""""
*Inherits from* :ref:`Property <v3.1_commons_Property>`

* Attributes:
	* ``value`` [String]

.. _v3.1_commons_Source:

Source
""""""
*Inherits from* :ref:`DOMLElement <v3.1_commons_DOMLElement>`

* Attributes:
	* ``entry`` [String]
	* ``inventory`` [String]
	* ``backend`` [String]

.. _v3.1_commons_UserPass:

UserPass
""""""""
*Inherits from* :ref:`Credentials <v3.1_commons_Credentials>`

* Attributes:
	* ``username`` [String]
	* ``password`` [String]

application
^^^^^^^^^^^

.. _v3.1_application_ApplicationComponent:

ApplicationComponent
""""""""""""""""""""
*Inherits from* :ref:`DeployableElement <v3.1_commons_DeployableElement>`


.. _v3.1_application_ApplicationLayer:

ApplicationLayer
""""""""""""""""
*Inherits from* :ref:`DOMLElement <v3.1_commons_DOMLElement>`

* Associations:
	* ``components`` → ApplicationComponent [0..*]

.. _v3.1_application_DBMS:

DBMS
""""
*Inherits from* :ref:`SoftwareComponent <v3.1_application_SoftwareComponent>`


.. _v3.1_application_SaaS:

SaaS
""""
*Inherits from* :ref:`ApplicationComponent <v3.1_application_ApplicationComponent>`

* Associations:
	* ``exposedInterfaces`` → SoftwareInterface [0..*]
* Attributes:
	* ``licenseCost`` [String]

.. _v3.1_application_SaaSDBMS:

SaaSDBMS
""""""""
*Inherits from* :ref:`SaaS <v3.1_application_SaaS>`

* Attributes:
	* ``databaseName`` [String]
	* ``engine`` [String]
	* ``engineVersion`` [String]

.. _v3.1_application_SoftwareComponent:

SoftwareComponent
"""""""""""""""""
*Inherits from* :ref:`ApplicationComponent <v3.1_application_ApplicationComponent>`

* Associations:
	* ``exposedInterfaces`` → SoftwareInterface [0..*]
	* ``consumedInterfaces`` → SoftwareInterface [0..*]
	* ``src`` → Source [0..1]
* Attributes:
	* ``isPersistent`` [Boolean]
	* ``licenseCost`` [String]

.. _v3.1_application_SoftwareInterface:

SoftwareInterface
"""""""""""""""""
*Inherits from* :ref:`ApplicationComponent <v3.1_application_ApplicationComponent>`

* Attributes:
	* ``endPoint`` [String]

infrastructure
^^^^^^^^^^^^^^

.. _v3.1_infrastructure_AutoScalingGroup:

AutoScalingGroup
""""""""""""""""
*Inherits from* :ref:`ComputingGroup <v3.1_infrastructure_ComputingGroup>`

* Associations:
	* ``machineDefinition`` → VirtualMachine [1..1]
* Attributes:
	* ``min`` [Integer]
	* ``max`` [Integer]
	* ``loadBalancer`` [String]

.. _v3.1_infrastructure_ComputingGroup:

ComputingGroup
""""""""""""""
*Inherits from* :ref:`DOMLElement <v3.1_commons_DOMLElement>`

* Associations:
	* ``groupedNodes`` → ComputingNode [0..*]

.. _v3.1_infrastructure_ComputingNode:

ComputingNode
"""""""""""""
*Inherits from* :ref:`Node <v3.1_infrastructure_Node>`

* Associations:
	* ``location`` → Location [0..1]
	* ``credentials`` → Credentials [0..1]
	* ``group`` → ComputingGroup [0..1]
	* ``nodeSpecificMonitoring`` → MonitoringRule [0..1]
* Attributes:
	* ``architecture`` [String]
	* ``os`` [String]
	* ``memory_mb`` [Integer]
	* ``memory_kb`` [Integer]
	* ``storage`` [Integer]
	* ``cpu_count`` [Integer]
	* ``cost`` [Integer]
	* ``disabledMonitorings`` [String]

.. _v3.1_infrastructure_ComputingNodeGenerator:

ComputingNodeGenerator
""""""""""""""""""""""
*Inherits from* :ref:`DOMLElement <v3.1_commons_DOMLElement>`

* Attributes:
	* ``uri`` [String]
	* ``kind`` [GeneratorKind]

.. _v3.1_infrastructure_Container:

Container
"""""""""
*Inherits from* :ref:`ComputingNode <v3.1_infrastructure_ComputingNode>`

* Associations:
	* ``generatedFrom`` → ContainerImage [0..1]
	* ``hostConfigs`` → ContainerHostConfig [0..*]
	* ``networks`` → ContainerNetwork [0..*]
	* ``volumes`` → ContainerVolume [0..*]
	* ``dependsOn`` → Container [0..*]

.. _v3.1_infrastructure_ContainerConfig:

ContainerConfig
"""""""""""""""
*Inherits from* :ref:`DOMLElement <v3.1_commons_DOMLElement>`

* Associations:
	* ``iface`` → NetworkInterface [0..1]
* Attributes:
	* ``container_port`` [Integer]
	* ``vm_port`` [Integer]

.. _v3.1_infrastructure_ContainerGroup:

ContainerGroup
""""""""""""""
*Inherits from* :ref:`ComputingGroup <v3.1_infrastructure_ComputingGroup>`

* Associations:
	* ``services`` → Container [1..*]
	* ``networks`` → ContainerNetwork [0..*]
	* ``volumes`` → ContainerVolume [0..*]

.. _v3.1_infrastructure_ContainerHostConfig:

ContainerHostConfig
"""""""""""""""""""
*Inherits from* :ref:`DOMLElement <v3.1_commons_DOMLElement>`

* Associations:
	* ``environment_variables`` → SProperty [0..*]
	* ``host`` → ComputingNode [0..1]
	* ``configurations`` → ContainerConfig [0..*]

.. _v3.1_infrastructure_ContainerImage:

ContainerImage
""""""""""""""
*Inherits from* :ref:`ComputingNodeGenerator <v3.1_infrastructure_ComputingNodeGenerator>`

* Associations:
	* ``generatedContainers`` → Container [0..*]

.. _v3.1_infrastructure_ContainerNetwork:

ContainerNetwork
""""""""""""""""
*Inherits from* :ref:`DOMLElement <v3.1_commons_DOMLElement>`

* Attributes:
	* ``containerNetworkName`` [String]

.. _v3.1_infrastructure_ContainerVolume:

ContainerVolume
"""""""""""""""
*Inherits from* :ref:`DOMLElement <v3.1_commons_DOMLElement>`

* Attributes:
	* ``containerVolumeName`` [String]
	* ``path`` [String]

.. _v3.1_infrastructure_ExecutionEnvironment:

ExecutionEnvironment
""""""""""""""""""""
*Inherits from* :ref:`InfrastructureElement <v3.1_infrastructure_InfrastructureElement>`

* Associations:
	* ``location`` → Location [0..1]
	* ``network`` → Network [0..1]
	* ``securityGroups`` → SecurityGroup [0..*]
* Attributes:
	* ``size`` [Integer]
	* ``maxSize`` [Integer]

.. _v3.1_infrastructure_ExtInfrastructureElement:

ExtInfrastructureElement
""""""""""""""""""""""""
*Inherits from* :ref:`InfrastructureElement <v3.1_infrastructure_InfrastructureElement>`


.. _v3.1_infrastructure_FunctionAsAService:

FunctionAsAService
""""""""""""""""""
*Inherits from* :ref:`InfrastructureElement <v3.1_infrastructure_InfrastructureElement>`

* Attributes:
	* ``cost`` [Integer]

.. _v3.1_infrastructure_InfrastructureElement:

InfrastructureElement
"""""""""""""""""""""
*Inherits from* :ref:`DeployableElement <v3.1_commons_DeployableElement>`


.. _v3.1_infrastructure_InfrastructureLayer:

InfrastructureLayer
"""""""""""""""""""
*Inherits from* :ref:`DOMLElement <v3.1_commons_DOMLElement>`

* Associations:
	* ``nodes`` → ComputingNode [0..*]
	* ``generators`` → ComputingNodeGenerator [0..*]
	* ``storages`` → Storage [0..*]
	* ``faas`` → FunctionAsAService [0..*]
	* ``credentials`` → Credentials [0..*]
	* ``groups`` → ComputingGroup [0..*]
	* ``securityGroups`` → SecurityGroup [0..*]
	* ``networks`` → Network [0..*]
	* ``rules`` → MonitoringRule [0..*]
	* ``executionEnvironments`` → ExecutionEnvironment [0..*]

.. _v3.1_infrastructure_InternetGateway:

InternetGateway
"""""""""""""""
*Inherits from* :ref:`Node <v3.1_infrastructure_Node>`

* Attributes:
	* ``address`` [String]

.. _v3.1_infrastructure_Location:

Location
""""""""
*Inherits from* :ref:`DOMLElement <v3.1_commons_DOMLElement>`

* Attributes:
	* ``region`` [String]
	* ``zone`` [String]

.. _v3.1_infrastructure_MonitoringRule:

MonitoringRule
""""""""""""""
*Inherits from* :ref:`DOMLElement <v3.1_commons_DOMLElement>`

* Attributes:
	* ``condition`` [String]
	* ``strategy`` [String]
	* ``strategyConfigurationString`` [String]

.. _v3.1_infrastructure_Network:

Network
"""""""
*Inherits from* :ref:`DOMLElement <v3.1_commons_DOMLElement>`

* Associations:
	* ``connectedIfaces`` → NetworkInterface [0..*]
	* ``gateways`` → InternetGateway [0..*]
	* ``subnets`` → Subnet [0..*]
* Attributes:
	* ``protocol`` [String]
	* ``cidr`` [Integer]

.. _v3.1_infrastructure_NetworkInterface:

NetworkInterface
""""""""""""""""
*Inherits from* :ref:`InfrastructureElement <v3.1_infrastructure_InfrastructureElement>`

* Associations:
	* ``belongsTo`` → Network [0..1]
	* ``associated`` → SecurityGroup [0..1]
* Attributes:
	* ``endPoint`` [Integer]
	* ``speed`` [String]

.. _v3.1_infrastructure_Node:

Node
""""
*Inherits from* :ref:`InfrastructureElement <v3.1_infrastructure_InfrastructureElement>`

* Associations:
	* ``ifaces`` → NetworkInterface [0..*]

.. _v3.1_infrastructure_PhysicalComputingNode:

PhysicalComputingNode
"""""""""""""""""""""
*Inherits from* :ref:`ComputingNode <v3.1_infrastructure_ComputingNode>`

* Associations:
	* ``configInterface`` → NetworkInterface [0..1]

.. _v3.1_infrastructure_Rule:

Rule
""""
*Inherits from* :ref:`DOMLElement <v3.1_commons_DOMLElement>`

* Attributes:
	* ``kind`` [String]
	* ``protocol`` [String]
	* ``fromPort`` [Integer]
	* ``toPort`` [Integer]
	* ``cidr`` [String]

.. _v3.1_infrastructure_SecurityGroup:

SecurityGroup
"""""""""""""
*Inherits from* :ref:`DOMLElement <v3.1_commons_DOMLElement>`

* Associations:
	* ``rules`` → Rule [0..*]
	* ``ifaces`` → NetworkInterface [0..*]

.. _v3.1_infrastructure_Storage:

Storage
"""""""
*Inherits from* :ref:`Node <v3.1_infrastructure_Node>`

* Attributes:
	* ``label`` [String]
	* ``size_gb`` [Integer]
	* ``cost`` [Integer]

.. _v3.1_infrastructure_Subnet:

Subnet
""""""
*Inherits from* :ref:`Network <v3.1_infrastructure_Network>`

* Associations:
	* ``connectedTo`` → Network [0..*]

.. _v3.1_infrastructure_Swarm:

Swarm
"""""
*Inherits from* :ref:`ComputingGroup <v3.1_infrastructure_ComputingGroup>`

* Associations:
	* ``roles`` → SwarmRole [0..*]

.. _v3.1_infrastructure_SwarmRole:

SwarmRole
"""""""""
*Inherits from* :ref:`DOMLElement <v3.1_commons_DOMLElement>`

* Associations:
	* ``nodes`` → ComputingNode [0..*]
* Attributes:
	* ``kind`` [String]

.. _v3.1_infrastructure_VMImage:

VMImage
"""""""
*Inherits from* :ref:`ComputingNodeGenerator <v3.1_infrastructure_ComputingNodeGenerator>`

* Associations:
	* ``generatedVMs`` → VirtualMachine [0..*]

.. _v3.1_infrastructure_VirtualMachine:

VirtualMachine
""""""""""""""
*Inherits from* :ref:`ComputingNode <v3.1_infrastructure_ComputingNode>`

* Associations:
	* ``generatedFrom`` → VMImage [0..1]
	* ``configInterface`` → NetworkInterface [0..1]
* Attributes:
	* ``sizeDescription`` [String]

concrete
^^^^^^^^

.. _v3.1_concrete_AutoScalingGroup:

AutoScalingGroup
""""""""""""""""
*Inherits from* :ref:`ConcreteElement <v3.1_concrete_ConcreteElement>`

* Associations:
	* ``maps`` → AutoScalingGroup [0..1]
* Attributes:
	* ``vm_type`` [String]

.. _v3.1_concrete_ConcreteElement:

ConcreteElement
"""""""""""""""
*Inherits from* :ref:`DOMLElement <v3.1_commons_DOMLElement>`

* Associations:
	* ``refs`` → ConcreteElement [0..*]
* Attributes:
	* ``resourceName`` [String]
	* ``configurationScript`` [String]
	* ``preexisting`` [Boolean]

.. _v3.1_concrete_ConcreteInfrastructure:

ConcreteInfrastructure
""""""""""""""""""""""
*Inherits from* :ref:`DOMLElement <v3.1_commons_DOMLElement>`

* Associations:
	* ``providers`` → RuntimeProvider [0..*]

.. _v3.1_concrete_ContainerImage:

ContainerImage
""""""""""""""
*Inherits from* :ref:`ConcreteElement <v3.1_concrete_ConcreteElement>`

* Associations:
	* ``maps`` → ContainerImage [0..1]

.. _v3.1_concrete_ExecutionEnvironment:

ExecutionEnvironment
""""""""""""""""""""
*Inherits from* :ref:`ConcreteElement <v3.1_concrete_ConcreteElement>`

* Associations:
	* ``maps`` → ExecutionEnvironment [0..1]
* Attributes:
	* ``instance_type`` [String]
	* ``storage_type`` [String]

.. _v3.1_concrete_FunctionAsAService:

FunctionAsAService
""""""""""""""""""
*Inherits from* :ref:`ConcreteElement <v3.1_concrete_ConcreteElement>`

* Associations:
	* ``maps`` → FunctionAsAService [0..1]

.. _v3.1_concrete_GenericResource:

GenericResource
"""""""""""""""
*Inherits from* :ref:`ConcreteElement <v3.1_concrete_ConcreteElement>`

* Attributes:
	* ``type`` [String]

.. _v3.1_concrete_Network:

Network
"""""""
*Inherits from* :ref:`ConcreteElement <v3.1_concrete_ConcreteElement>`

* Associations:
	* ``subnets`` → Subnet [0..*]
	* ``maps`` → Network [0..1]
* Attributes:
	* ``protocol`` [String]
	* ``addressRange`` [String]

.. _v3.1_concrete_RuntimeProvider:

RuntimeProvider
"""""""""""""""
*Inherits from* :ref:`DOMLElement <v3.1_commons_DOMLElement>`

* Associations:
	* ``resources`` → GenericResource [0..*]
	* ``vms`` → VirtualMachine [0..*]
	* ``executionEnvironments`` → ExecutionEnvironment [0..*]
	* ``vmImages`` → VMImage [0..*]
	* ``containerImages`` → ContainerImage [0..*]
	* ``networks`` → Network [0..*]
	* ``storages`` → Storage [0..*]
	* ``faas`` → FunctionAsAService [0..*]
	* ``autoScalingGroups`` → AutoScalingGroup [0..*]

.. _v3.1_concrete_Storage:

Storage
"""""""
*Inherits from* :ref:`ConcreteElement <v3.1_concrete_ConcreteElement>`

* Associations:
	* ``maps`` → Storage [0..1]

.. _v3.1_concrete_Subnet:

Subnet
""""""
*Inherits from* :ref:`Network <v3.1_concrete_Network>`


.. _v3.1_concrete_VMImage:

VMImage
"""""""
*Inherits from* :ref:`ConcreteElement <v3.1_concrete_ConcreteElement>`

* Associations:
	* ``maps`` → VMImage [0..1]
* Attributes:
	* ``image_name`` [String]

.. _v3.1_concrete_VirtualMachine:

VirtualMachine
""""""""""""""
*Inherits from* :ref:`ConcreteElement <v3.1_concrete_ConcreteElement>`

* Associations:
	* ``maps`` → VirtualMachine [0..1]
* Attributes:
	* ``vm_type`` [String]



