from Tests.VDownloaderTests import VulkanDownloaderTest
from Tests.VSpotifyTests import VulkanSpotifyTest
from Tests.VDeezerTests import VulkanDeezerTest


tester = VulkanDownloaderTest()
tester.run()
tester = VulkanSpotifyTest()
tester.run()
tester = VulkanDeezerTest()
tester.run()
