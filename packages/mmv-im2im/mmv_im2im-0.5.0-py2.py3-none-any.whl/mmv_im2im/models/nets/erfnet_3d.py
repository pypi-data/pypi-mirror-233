import torch
import torch.nn as nn
import torch.nn.functional as F


class DownsamplerBlock(nn.Module):
    def __init__(self, ninput, noutput):
        super().__init__()

        self.conv = nn.Conv3d(
            ninput, noutput - ninput, (3, 3, 3), stride=2, padding=1, bias=True
        )

        self.pool = nn.MaxPool3d(2, stride=2)

        self.bn = nn.BatchNorm3d(noutput, eps=1e-3)

    def forward(self, input):
        output = torch.cat([self.conv(input), self.pool(input)], 1)
        output = self.bn(output)
        return F.relu(output)


class non_bottleneck_1d(nn.Module):
    def __init__(self, chann, dropprob, dilated):
        super().__init__()
        self.conv3x1x1_1 = nn.Conv3d(
            chann, chann, (3, 1, 1), stride=1, padding=(1, 0, 0), bias=True
        )

        self.conv1x3x1_1 = nn.Conv3d(
            chann, chann, (1, 3, 1), stride=1, padding=(0, 1, 0), bias=True
        )

        self.conv1x1x3_1 = nn.Conv3d(
            chann, chann, (1, 1, 3), stride=1, padding=(0, 0, 1), bias=True
        )

        self.bn1 = nn.BatchNorm3d(chann, eps=1e-03)

        self.conv3x1x1_2 = nn.Conv3d(
            chann,
            chann,
            (3, 1, 1),
            stride=1,
            padding=(1 * dilated, 0, 0),
            bias=True,
            dilation=(dilated, 1, 1),
        )

        self.conv1x3x1_2 = nn.Conv3d(
            chann,
            chann,
            (1, 3, 1),
            stride=1,
            padding=(0, 1 * dilated, 0),
            bias=True,
            dilation=(1, dilated, 1),
        )

        self.conv1x1x3_2 = nn.Conv3d(
            chann,
            chann,
            (1, 1, 3),
            stride=1,
            padding=(0, 0, 1 * dilated),
            bias=True,
            dilation=(1, 1, dilated),
        )

        self.bn2 = nn.BatchNorm3d(chann, eps=1e-03)

        self.dropout = nn.Dropout3d(dropprob)

    def forward(self, input):
        output = self.conv3x1x1_1(input)
        output = F.relu(output)
        output = self.conv1x3x1_1(output)
        output = F.relu(output)
        output = self.conv1x1x3_1(output)
        # TODO think about adding a relu here!

        output = self.bn1(output)
        output = F.relu(output)

        output = self.conv3x1x1_2(output)
        output = F.relu(output)
        output = self.conv1x3x1_2(output)
        output = F.relu(output)
        output = self.conv1x1x3_2(output)
        output = self.bn2(output)

        if self.dropout.p != 0:
            output = self.dropout(output)

        return F.relu(output + input)  # +input = identity (residual connection)


class Encoder(nn.Module):
    def __init__(self, num_classes, input_channels):
        super().__init__()
        self.initial_block = DownsamplerBlock(input_channels, 16)

        self.layers = nn.ModuleList()

        self.layers.append(DownsamplerBlock(16, 64))

        for x in range(0, 5):  # 5 times
            self.layers.append(non_bottleneck_1d(64, 0.03, 1))

        self.layers.append(DownsamplerBlock(64, 128))

        for x in range(0, 2):  # 2 times
            self.layers.append(non_bottleneck_1d(128, 0.3, 2))
            self.layers.append(non_bottleneck_1d(128, 0.3, 4))
            self.layers.append(non_bottleneck_1d(128, 0.3, 8))
            self.layers.append(non_bottleneck_1d(128, 0.3, 16))

        self.output_conv = nn.Conv3d(
            128, num_classes, 1, stride=1, padding=0, bias=True
        )

    def forward(self, input, predict=False):
        output = self.initial_block(input)

        for layer in self.layers:
            output = layer(output)

        if predict:
            output = self.output_conv(output)

        return output


class UpsamplerBlock(nn.Module):
    def __init__(self, ninput, noutput):
        super().__init__()
        self.conv = nn.ConvTranspose3d(
            ninput, noutput, 3, stride=2, padding=1, output_padding=1, bias=True
        )
        self.bn = nn.BatchNorm3d(noutput, eps=1e-3)

    def forward(self, input):
        output = self.conv(input)
        output = self.bn(output)
        return F.relu(output)


class Decoder(nn.Module):
    def __init__(self, num_classes):
        super().__init__()

        self.layers = nn.ModuleList()

        self.layers.append(UpsamplerBlock(128, 64))
        self.layers.append(non_bottleneck_1d(64, 0, 1))
        self.layers.append(non_bottleneck_1d(64, 0, 1))

        self.layers.append(UpsamplerBlock(64, 16))
        self.layers.append(non_bottleneck_1d(16, 0, 1))
        self.layers.append(non_bottleneck_1d(16, 0, 1))

        self.output_conv = nn.ConvTranspose3d(
            16, num_classes, 2, stride=2, padding=0, output_padding=0, bias=True
        )

    def forward(self, input):
        output = input

        for layer in self.layers:
            output = layer(output)

        output = self.output_conv(output)

        return output


# ERFNet
class Net(nn.Module):
    def __init__(
        self, num_classes, input_channels, encoder=None
    ):  # use encoder to pass pretrained encoder
        super().__init__()

        if encoder is None:
            self.encoder = Encoder(num_classes, input_channels)
        else:
            self.encoder = encoder
        self.decoder = Decoder(num_classes)

    def forward(self, input, only_encode=False):
        if only_encode:
            return self.encoder.forward(input, predict=True)
        else:
            output = self.encoder(input)  # predict=False by default
            return self.decoder.forward(output)
