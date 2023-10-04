from baby_steps import then, when

from vedro_dependency_finder import DependencyFinder, DependencyFinderPlugin


def test_plugin():
    with when:
        plugin = DependencyFinderPlugin(DependencyFinder)

    with then:
        assert isinstance(plugin, DependencyFinderPlugin)
