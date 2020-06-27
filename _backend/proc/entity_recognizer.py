"""
@author : Hyunwoong
@when : 6/20/2020
@homepage : https://github.com/gusdnd852
"""
import torch
from torch import nn
from torch import Tensor

from _backend.decorators import entity
from _backend.loss.base.base_loss import BaseLoss
from _backend.loss.crf_loss import CRFLoss
from _backend.loss.utils.masking import Masking
from _backend.proc.base.torch_processor import TorchProcessor


@entity
class EntityRecognizer(TorchProcessor):

    def __init__(self, model: nn.Module, loss: BaseLoss, masking: bool = True):

        """
        개체명 인식 (Named Entity Recognition) 모델을 학습시키고
        테스트 및 추론을 진행합니다. Loss함수를 변경해서 CRF를 추가할 수 있습니다.

        :param model: NER 모델
        :param loss: Loss 함수 종류
        :param masking: Loss 계산시 masking 여부
        """

        self.label_dict = model.label_dict
        self.loss = loss.to(self.device)
        self.masking = Masking() if masking else None
        self.parameters = list(model.parameters())

        if len(list(loss.parameters())) != 0:
            self.parameters += list(loss.parameters())

        super().__init__(model, self.parameters)

    def predict(self, sequence: Tensor) -> list:
        """
        사용자의 입력에 inference합니다.
        
        :param sequence: 입력 시퀀스
        :return: 분류 결과 (엔티티 시퀀스) 리턴
        """

        self._load_model()
        self.model.eval()

        # pad는 전부 0이니까 입력 전체에 1을 더하고,
        # all()로 체크하면 pad만 True가 나옴. (모두 1이여야 True)
        # 이 때 False 갯수를 세면 pad가 아닌 부분의 길이가 됨.
        length = [all(map(int, (i + 1).tolist()))
                  for i in sequence.squeeze()].count(False)

        predicts = self._forward(sequence).squeeze().t()
        predicts = [list(self.label_dict.keys())[i.item()]  # 라벨 딕셔너리에서 i번째 원소를 담음
                    for i in predicts]  # 분류 예측결과에서 i를 하나씩 꺼내서

        return predicts[:length]

    def _train_epoch(self, epoch: int) -> tuple:
        """
        학습시 1회 에폭에 대한 행동을 정의합니다.

        :param epoch: 현재 에폭
        :return: 평균 loss, 예측 리스트, 라벨 리스트
        """

        loss_list, predict_list, label_list = [], [], []
        self.model.train()

        for feats, labels, lengths in self.train_data:
            feats, labels = feats.to(self.device), labels.to(self.device)
            predicts, losses = self._forward(feats, labels, lengths)
            losses = self._backward(losses)

            loss_list.append(losses)
            predict_list.append(predicts)
            label_list.append(labels)

        losses = sum(loss_list) / len(loss_list)
        predicts = torch.flatten(torch.cat(predict_list, dim=0))
        labels = torch.flatten(torch.cat(label_list, dim=0))
        return losses, predicts, labels

    def _test_epoch(self, epoch: int) -> tuple:
        """
        테스트시 1회 에폭에 대한 행동을 정의합니다.

        :param epoch: 현재 에폭
        :return: 평균 loss, 예측 리스트, 라벨 리스트
        """

        loss_list, predict_list, label_list = [], [], []
        self.model.eval()

        for feats, labels, lengths in self.test_data:
            feats, labels = feats.to(self.device), labels.to(self.device)
            predicts, losses = self._forward(feats, labels, lengths)

            loss_list.append(losses)
            predict_list.append(predicts)
            label_list.append(labels)

        losses = sum(loss_list) / len(loss_list)
        predicts = torch.flatten(torch.cat(predict_list, dim=0))
        labels = torch.flatten(torch.cat(label_list, dim=0))
        return losses, predicts, labels

    def _forward(self, feats: Tensor, labels: Tensor = None, length: Tensor = None):

        """
        모델의 feed forward에 대한 행동을 정의합니다.

        :param feats: 입력 feature
        :param labels: label 리스트
        :param lengths: 패딩을 제외한 입력의 길이 리스트
        :return: 모델의 예측, loss
        """

        logits = self.model(feats)

        if isinstance(self.loss, CRFLoss):
            # CRF인 경우, Viterbi Decoding으로 Inference 해야함.
            predicts = torch.tensor(self.loss.decode(logits))
        else:
            predicts = torch.tensor(torch.max(logits, dim=1)[1])

        if labels is None:
            return predicts
        else:
            mask = self.masking(length) if self.masking else None
            loss = self.loss.compute_loss(labels, logits, feats, mask)
            return predicts, loss
