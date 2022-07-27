from Music.VulkanInitializer import VulkanInitializer


if __name__ == '__main__':
    initializer = VulkanInitializer(willListen=True)
    vulkanBot = initializer.getBot()
    vulkanBot.startBot()
