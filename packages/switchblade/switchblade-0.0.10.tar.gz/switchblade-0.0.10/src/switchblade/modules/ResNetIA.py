'''
ResNetIA.py: ResNet architecture with intermediate activations
'''

import torch
import torch.nn as nn

class BasicBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super(BasicBlock, self).__init__()

        self.residual_function = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(out_channels)
        )

        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )

    def forward(self, x):
        return nn.ReLU(inplace=True)(self.residual_function(x) + self.shortcut(x))


class ResNet(nn.Module):
    def __init__(self, block, num_block, num_classes=10, in_channels=3):
        super(ResNet, self).__init__()

        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels, 64, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True)
        )

        self.in_channels = 64

        self.conv2_x = self._make_layer(block, 64, num_block[0], 1)
        self.conv3_x = self._make_layer(block, 128, num_block[1], 2)
        self.conv4_x = self._make_layer(block, 256, num_block[2], 2)
        self.conv5_x = self._make_layer(block, 512, num_block[3], 2)

        self.avg_pool1 = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 2)),
            nn.Flatten()
        )
        self.avg_pool2 = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten()
        )
        self.avg_pool3 = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.AdaptiveAvgPool1d(128)
        )
        self.avg_pool4 = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.AdaptiveAvgPool1d(128)
        )
        self.fc = nn.Linear(512, num_classes)

    def _make_layer(self, block, out_channels, num_blocks, stride):
        strides = [stride] + [1] * (num_blocks - 1)
        layers = []
        for stride in strides:
            layers.append(block(self.in_channels, out_channels, stride))
            self.in_channels = out_channels
        return nn.Sequential(*layers)

    def forward(self, x):
        output = self.conv1(x)

        activations = []

        # block 1
        output = self.conv2_x(output)
        activations.append(self.avg_pool1(output))

        # block 2
        output = self.conv3_x(output)
        activations.append(self.avg_pool2(output))

        # block 3
        output = self.conv4_x(output)
        activations.append(self.avg_pool3(output))

        # block 4
        output = self.conv5_x(output)
        activations.append(self.avg_pool4(output))

        output = torch.cat(activations, dim=1)
        output = self.fc(output)

        return output

    @property
    def n_params(self):
        return sum(p.numel() for p in self.parameters())


def resnet18_ia(**kwargs) -> ResNet:
    """Constructs a ResNet-18 model."""
    model = ResNet(BasicBlock, [2, 2, 2, 2], **kwargs)
    return model

def resnet34_ia(**kwargs) -> ResNet:
    """Constructs a ResNet-34 model."""
    model = ResNet(BasicBlock, [3, 4, 6, 3], **kwargs)
    return model

def resnet50_ia(**kwargs) -> ResNet:
    """Constructs a ResNet-50 model."""
    model = ResNet(BasicBlock, [3, 4, 6, 3], **kwargs)
    return model