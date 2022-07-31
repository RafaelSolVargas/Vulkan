from Music.VulkanInitializer import VulkanInitializer
from Config.Folder import Folder

if __name__ == '__main__':
    folder = Folder()
    initializer = VulkanInitializer(willListen=True)
    vulkanBot = initializer.getBot()
    vulkanBot.startBot()
