import {
  Model,
  ModelFoundationEnum,
  ModelDownloadProgressStatusEnum,
} from '../../PiecesSDK/core';
import Constants from '../../const';
import Modal from './Modal';
import ModelProgressController from '../../connection/ModelProgressController';
import ProgressBar from '../render/ProgressBar';
import { ProgressBarLocation } from '../../models/ProgressBarLocation';
import { timeoutPromise } from '../utils/timeoutPromise';
import ConnectorSingleton from '../../connection/connector_singleton';
import Notifications from '../../connection/notification_handler';
import PiecesDatabase from '../../database/PiecesDatabase';

enum ModelBoxEnum {
  LLaMa2 = 'Llama2',
  CodeLlaMa = 'CodeLlama',
  OpenAi = 'Open AI',
}

export default class CopilotLLMConfigModal extends Modal {
  public static selectedRuntime: 'CPU' | 'GPU' | 'CLOUD' = 'CLOUD';

  public static selectedModel = '';

  private activeModelPill: HTMLElement | undefined;

  private modelButtons: {
    selected: boolean;
    btn: HTMLElement;
    model: string;
  }[] = [];

  async onOpen() {
    this.modelButtons = [];
    const modelProgress = ModelProgressController.getInstance();
    modelProgress.registerCallback(this.refresh);
    const models = await modelProgress.models;
    modelProgress.openSockets(
      models.iterable.filter(
        (el) =>
          el.foundation === ModelFoundationEnum.Llama27B &&
          el.unique !== 'llama-2-7b-chat.ggmlv3.q4_K_M'
      )
    );

    if (!CopilotLLMConfigModal.selectedModel) {
      CopilotLLMConfigModal.selectedModel = models.iterable.find(
        (el) => el.unique === 'gpt-3.5-turbo'
      )!.id;
    }

    this.contentEl.empty();
    this.contentEl.classList.add('min-h-[50vh]', '!flex', 'flex-col');

    this.titleEl.innerText = 'Copilot Runtime';
    this.contentEl.appendChild(this.titleEl);
    const titleDesc = this.titleEl.createEl('p');
    titleDesc.classList.add(
      'm-0',
      'text-xs',
      'font-normal',
      'text-[var(--text-faint)]'
    );
    titleDesc.innerText = "Choose between different LLM's and runtime types";

    const container = this.contentEl.createDiv();
    container.classList.add(
      'flex',
      'flex-col',
      'w-full',
      'h-full',
      'flex-grow'
    );

    const tabs = container.createDiv();
    tabs.classList.add('flex-row', 'justify-around', 'flex', 'py-3');

    const cloudModels = container.createDiv();
    cloudModels.classList.add(
      'hidden',
      'flex',
      'w-full',
      'h-full',
      'flex-col',
      'gap-3',
      'flex-grow'
    );

    const localModels = container.createDiv();
    localModels.classList.add(
      'flex',
      'w-full',
      'h-full',
      'flex-col',
      'gap-3',
      'flex-grow'
    );

    const localRecommendation = localModels.createDiv(); // recommendation for local models
    localRecommendation.classList.add(
      'flex',
      'flex-col',
      'rounded-md',
      'p-2',
      'bg-[var(--background-modifier-border)]',
      'gap-2',
      'cursor-pointer',
      'hover:bg-[var(--background-modifier-border-hover)]'
    );

    const recommendationTitleRow = localRecommendation.createDiv();
    recommendationTitleRow.classList.add(
      'flex',
      'flex-row',
      'justify-between',
      'items-center',
      'px-[2px]'
    );

    const recommendationTitle = recommendationTitleRow.createEl('p');
    recommendationTitle.classList.add(
      'font-light',
      'text-[var(--text-faint)]',
      'm-0',
      'text-xs'
    );
    recommendationTitle.innerText = 'MODEL RECOMMENDATIONS';

    const recommendationCaret = recommendationTitleRow.createEl('p');
    recommendationCaret.classList.add('m-0', 'text-xs', 'font-semibold');
    recommendationCaret.innerHTML = '▼';

    const recommendationExpandContainer = localRecommendation.createDiv();
    recommendationExpandContainer.classList.add('hidden');

    localRecommendation.onclick = (e) => {
      recommendationExpandContainer.classList.toggle('hidden');
      recommendationCaret.innerHTML =
        recommendationExpandContainer.classList.contains('hidden')
          ? '▼'
          : '&times;';
      e.stopPropagation();
    };

    // recommendation description
    const recommendationDesc = recommendationExpandContainer.createEl('p');
    recommendationDesc.classList.add(
      'm-0',
      'text-[var(--text-muted)]',
      'text-sm'
    );
    recommendationDesc.innerText =
      "Local LLM's are not recommended for low power or older machines, to ensure a good experience please follow the recommended practices for choosing a model.";

    // list of recommendations
    const recommendationList = recommendationExpandContainer.createEl('ul');
    recommendationList.classList.add(
      'text-xs',
      '!list-disc',
      'text-[var(--text-faint)]',
      'pl-3',
      'gap-1',
      'flex',
      'flex-col'
    );
    const gpuRecommendation = recommendationList.createEl('li');
    gpuRecommendation.innerHTML =
      "<strong>GPU</strong> LLM's are designed for machines with a modern, dedicated graphics chip (i.e: ARM Mac, NVIDIA GPU with 6gb VRAM or more)";
    const cpuRecommendation = recommendationList.createEl('li');
    cpuRecommendation.innerHTML =
      "<strong>CPU</strong> models are recommended if you do not have a strong enough graphics card for the GPU LLM's. Be aware this model will be as slow or as fast as your machine specs allow.";
    const cloudRecommendation = recommendationList.createEl('li');
    cloudRecommendation.innerHTML =
      '<strong>CLOUD</strong> models are recommended if performance issues arise while using the local models (for older or lower powered machines).';

    this.createModelBox(
      ModelBoxEnum.LLaMa2,
      localModels,
      models.iterable.filter(
        (el) =>
          el.foundation === ModelFoundationEnum.Llama27B &&
          !el.name.includes('CodeLlama')
      )
    );
    this.createModelBox(
      ModelBoxEnum.CodeLlaMa,
      localModels,
      models.iterable.filter((el) => el.name.includes('CodeLlama'))
    );
    this.createModelBox(
      ModelBoxEnum.OpenAi,
      cloudModels,
      models.iterable.filter(
        (el) =>
          el.foundation === ModelFoundationEnum.Gpt35 ||
          el.foundation === ModelFoundationEnum.Gpt4
      )
    );

    const localTab = tabs.createDiv();
    const cloudTab = tabs.createDiv();

    const localSvgBox = localTab.createDiv();
    localSvgBox.classList.add('h-4', 'svg-box');
    localSvgBox.innerHTML = Constants.LAPTOP_SVG;

    const localTabText = localTab.createEl('p');
    localTabText.classList.add('m-0');
    localTabText.innerText = 'On-Device';

    localTab.classList.add(
      'cursor-pointer',
      'underline',
      'flex',
      'flex-row',
      'gap-1',
      'items-center'
    );
    localTab.onclick = () => {
      localTab.classList.add('underline');
      cloudTab.classList.remove('underline');
      localModels.classList.remove('hidden');
      cloudModels.classList.add('hidden');
    };

    const cloudSvgBox = cloudTab.createDiv();
    cloudSvgBox.classList.add('svg-box', 'h-4');
    cloudSvgBox.innerHTML = Constants.CLOUD_SVG;

    const cloudTabText = cloudTab.createEl('p');
    cloudTabText.classList.add('m-0');
    cloudTabText.innerText = 'Cloud';

    cloudTab.classList.add(
      'cursor-pointer',
      'flex',
      'flex-row',
      'gap-1',
      'items-center'
    );
    cloudTab.onclick = () => {
      cloudTab.classList.add('underline');
      localTab.classList.remove('underline');
      localModels.classList.add('hidden');
      cloudModels.classList.remove('hidden');
    };

    const activeModel = this.contentEl.createDiv();
    activeModel.classList.add('flex', 'flex-col', 'h-full', 'gap-2', 'pt-2');

    const activeModelText = activeModel.createEl('p');
    activeModelText.classList.add('text-xs', 'text-[var(--text-faint)]', 'm-0');
    activeModelText.innerText = 'ACTIVE MODEL';

    const activeModelPill = activeModel.createDiv();
    activeModelPill.classList.add(
      'border-solid',
      'border',
      'rounded-lg',
      'p-2',
      'w-fit',
      'border-[var(--text-faint)]',
      'flex-row',
      'flex',
      'gap-2',
      'items-center'
    );
    const selectedModel =
      models.iterable.find(
        (el) => el.id === CopilotLLMConfigModal.selectedModel
      ) ?? models.iterable.find((el) => el.unique === 'gpt-3.5-turbo');
    activeModelPill.innerHTML = this.getModelName(selectedModel!);
    this.activeModelPill = activeModelPill;
  }

  createModelBox = (
    type: ModelBoxEnum,
    container: HTMLElement,
    models: Model[]
  ) => {
    const modelBox = container.createDiv();
    modelBox.classList.add(
      'border-solid',
      'border-[var(--text-faint)]',
      'rounded-md',
      'flex',
      'flex-col',
      'cursor-pointer',
      'p-2',
      'border',
      'gap-2'
    );

    const modelTitle = modelBox.createDiv();
    modelTitle.classList.add('flex-row', 'flex', 'items-center');

    const modelTitleText = modelTitle.createEl('div');
    modelTitleText.classList.add(
      'm-0',
      'flex',
      'flex-row',
      'gap-2',
      'items-center'
    );

    const svgBox = modelTitleText.createDiv();
    svgBox.classList.add('h-3', 'svg-box');
    svgBox.innerHTML = this.getModelSvg(type);

    const modelTitleTextType = modelTitleText.createEl('p');
    modelTitleTextType.classList.add('m-0');
    modelTitleTextType.innerText = type;

    const modelExpand = modelTitle.createDiv();
    modelExpand.classList.add('ml-auto', 'text-xs', 'font-semibold');
    modelExpand.innerHTML = '▼';

    const modelDesc = modelBox.createEl('p');
    modelDesc.classList.add('text-xs', 'text-[var(--text-faint)]', 'm-0');
    modelDesc.innerText = this.getOrgDesc(type);

    const modelElements = modelBox.createDiv();
    modelElements.classList.add('hidden', 'gap-2', 'flex', 'flex-col');

    const modelElementsText = modelElements.createEl('p');
    modelElementsText.classList.add(
      'm-0',
      'font-light',
      'text-xs',
      'text-[var(--text-faint)]',
      'pt-1'
    );
    modelElementsText.innerText = 'SELECT MODEL';

    this.buildModelElements(modelElements, models);

    modelBox.onclick = () => {
      const expanded = modelExpand.innerHTML === '▼';
      modelExpand.innerHTML = expanded ? '&times;' : '▼';
      modelElements.classList.toggle('hidden');
    };
  };

  async buildModelElements(containerEl: HTMLElement, models: Model[]) {
    for (let i = 0; i < models.length; i++) {
      this.buildModelElement(models[i], containerEl);
    }
  }

  buildModelElement(model: Model, containerEl: HTMLElement) {
    if (model.cloud) model.downloaded = true;
    const modelElement = containerEl.createDiv();
    modelElement.classList.add(
      'flex',
      'flex-col',
      'rounded-md',
      'p-2',
      'bg-[var(--background-modifier-border)]',
      'gap-2'
    );

    const modelTitleRow = modelElement.createDiv();
    modelTitleRow.classList.add(
      'flex',
      'flex-row',
      'justify-between',
      'items-center'
    );

    const modelTitle = modelTitleRow.createEl('p');
    modelTitle.innerText = this.getModelTitle(model);
    modelTitle.classList.add('m-0');

    const modelButton = modelTitleRow.createDiv();
    this.modelButtons.push({
      btn: modelButton,
      selected: CopilotLLMConfigModal.selectedModel === model.id,
      model: model.id,
    });
    modelButton.classList.add(
      'cursor-pointer',
      'hover:text-[var(--text-accent)]',
      'flex',
      'items-center',
      'text-xs'
    );

    const status =
      ModelProgressController.getInstance().modelDownloadStatus.get(model.id);

    if (model.name.includes('CodeLlama')) {
      modelButton.innerHTML = 'Coming Soon';
    } else if (model.downloaded) {
      modelButton.innerHTML = Constants.PLUG_SVG;
      modelButton.title = `Select ${modelTitle.innerText}`;
    } else if (
      status === ModelDownloadProgressStatusEnum.InProgress ||
      status === ModelDownloadProgressStatusEnum.Initialized
    ) {
      modelButton.innerHTML = '&times;';
      modelButton.title = `Cancel ${modelTitle.innerText} download`;
    } else {
      modelButton.innerHTML = Constants.DOWNLOAD_SVG;
      modelButton.title = `Download ${modelTitle.innerText}`;
    }

    if (CopilotLLMConfigModal.selectedModel === model.id) {
      modelButton.style.color = 'var(--text-accent)';
      modelButton.innerHTML = Constants.CHECK_SVG;
    }

    const modelRequirementsButton = modelElement.createDiv();
    modelRequirementsButton.classList.add(
      'cursor-pointer',
      'text-xs',
      'text-[var(--text-faint)]'
    );
    modelRequirementsButton.innerText = 'System Requirements  ▼';

    const modelRequirements = modelElement.createEl('p');
    modelRequirements.classList.add(
      'hidden',
      'text-xs',
      'pt-1',
      'text-[var(--text-faint)]',
      'm-0'
    );
    modelRequirements.innerText = this.getModelRequirements(model);

    modelRequirementsButton.onclick = (e) => {
      modelRequirementsButton.innerText = modelRequirements.classList.contains(
        'hidden'
      )
        ? 'System Requirements  ▲'
        : 'System Requirements  ▼';
      modelRequirements.classList.toggle('hidden');
      e.stopPropagation();
    };

    const progressBar = new ProgressBar({
      current: 0,
      end: 100,
      contentEl: modelElement,
      source: ProgressBarLocation.LLM_CONFIG,
    });
    if (
      status === ModelDownloadProgressStatusEnum.InProgress ||
      status === ModelDownloadProgressStatusEnum.Initialized
    ) {
      progressBar.bounce();
    } else {
      progressBar.hide();
    }

    modelButton.onclick = (e) => {
      e.stopPropagation();
      if (model.name.includes('CodeLlama')) {
        Notifications.getInstance().information({
          message:
            'The CodeLlama models are not quite ready for production, but are coming soon!',
        });
        return;
      }
      this.handleDownloadSelectCancel(model);

      timeoutPromise(200).then(() => {
        const newStatus =
          ModelProgressController.getInstance().modelDownloadStatus.get(
            model.id
          );
        if (model.downloaded) {
          this.setModelButtonsColor();
          modelButton.innerHTML = Constants.CHECK_SVG;
          modelButton.title = `Select ${modelTitle.innerText}`;
          const buttonObj = this.modelButtons.find(
            (el) => el.model === model.id
          );
          if (buttonObj) buttonObj.selected = true;
          modelButton.style.color = 'var(--text-accent)';
          this.activeModelPill!.innerHTML = this.getModelName(model);
        } else if (
          newStatus === ModelDownloadProgressStatusEnum.InProgress ||
          newStatus === ModelDownloadProgressStatusEnum.Initialized
        ) {
          modelButton.innerHTML = '&times;';
          modelButton.title = `Cancel ${modelTitle.innerText} download`;
          progressBar.show();
          progressBar.bounce();
        } else {
          modelButton.innerHTML = Constants.DOWNLOAD_SVG;
          modelButton.title = `Download ${modelTitle.innerText}`;
          progressBar.hide();
        }
      });
    };
  }

  setModelButtonsColor = () => {
    for (const btn of this.modelButtons) {
      if (btn.selected) {
        btn.btn.innerHTML = Constants.PLUG_SVG;
        btn.selected = false;
      }
      btn.btn.style.color = '';
    }
  };

  getOrgDesc = (type: ModelBoxEnum) => {
    if (type === ModelBoxEnum.LLaMa2) {
      return "Meta's fastest model in the Llama 2 family optimized to run on your device for a fast, air-gapped experience.";
    }
    if (type === ModelBoxEnum.CodeLlaMa) {
      return "Meta's model trained on top of Llama 2 fine-tuned for code-related tasks, optimized to run on your device.";
    }
    return "OpenAI's most capable and cost effective models. Includes up to 4,096 max tokens and has training data up until September 2021.";
  };

  getModelRequirements = (model: Model) => {
    if (model.cpu && model.foundation === ModelFoundationEnum.Llama27B)
      return '- requires at least 5.6GB RAM';

    if (!model.cpu && model.foundation === ModelFoundationEnum.Llama27B)
      return '- requires at least 5.6GB VRAM (GPU RAM)';

    return 'No local device requirements, runs solely in the cloud';
  };

  getModelTitle = (model: Model) => {
    if (
      model.cpu &&
      model.foundation === ModelFoundationEnum.Llama27B &&
      !model.name.includes('CodeLlama')
    )
      return '7B';

    if (
      !model.cpu &&
      model.foundation === ModelFoundationEnum.Llama27B &&
      !model.name.includes('CodeLlama')
    )
      return '7B GPU';

    if (model.cpu && model.name.includes('CodeLlama')) return '7B';

    if (!model.cpu && model.name.includes('CodeLlama')) return '7B GPU';

    if (model.foundation === ModelFoundationEnum.Gpt4) return 'GPT 4';

    if (model.name.includes('16k')) return 'GPT 3.5 16k';

    return 'GPT 3.5 Turbo';
  };

  getModelName = (model: Model) => {
    const svgBox = document.createElement('div');
    svgBox.classList.add('h-4', 'w-auto', 'svg-box');
    const textBox = document.createElement('p');
    textBox.classList.add('m-0');

    if (
      model.cpu &&
      model.foundation === ModelFoundationEnum.Llama27B &&
      !model.name.includes('CodeLlama')
    ) {
      svgBox.innerHTML = Constants.META_SVG;
      textBox.innerText = 'Llama2 7B CPU';
      return svgBox.outerHTML + textBox.outerHTML;
    }

    if (
      !model.cpu &&
      model.foundation === ModelFoundationEnum.Llama27B &&
      !model.name.includes('CodeLlama')
    ) {
      svgBox.innerHTML = Constants.META_SVG;
      textBox.innerText = 'Llama2 7B GPU';
      return svgBox.outerHTML + textBox.outerHTML;
    }

    if (model.cpu && model.name.includes('CodeLlama')) {
      svgBox.innerHTML = Constants.META_SVG;
      textBox.innerText = 'CodeLlama 7B CPU';
      return svgBox.outerHTML + textBox.outerHTML;
    }

    if (!model.cpu && model.name.includes('CodeLlama')) {
      svgBox.innerHTML = Constants.META_SVG;
      textBox.innerText = 'CodeLlama 7B GPU';
      return svgBox.outerHTML + textBox.outerHTML;
    }

    if (model.name.includes('16k')) {
      svgBox.innerHTML = Constants.OPENAI_SVG;
      textBox.innerText = 'GPT 3.5 16k';
      return svgBox.outerHTML + textBox.outerHTML;
    }

    if (model.foundation === ModelFoundationEnum.Gpt4) {
      svgBox.innerHTML = Constants.OPENAI_SVG;
      textBox.innerText = 'GPT 4';
      return svgBox.outerHTML + textBox.outerHTML;
    }

    svgBox.innerHTML = Constants.OPENAI_SVG;
    textBox.innerText = 'GPT 3.5 Turbo';
    return svgBox.outerHTML + textBox.outerHTML;
  };

  getModelSvg(type: ModelBoxEnum) {
    if (type === ModelBoxEnum.CodeLlaMa || type === ModelBoxEnum.LLaMa2) {
      return Constants.META_SVG;
    }
    return Constants.OPENAI_SVG;
  }

  handleDownloadSelectCancel(model: Model) {
    const status =
      ModelProgressController.getInstance().modelDownloadStatus.get(model.id);
    const config = ConnectorSingleton.getInstance();

    if (
      status === ModelDownloadProgressStatusEnum.InProgress ||
      status === ModelDownloadProgressStatusEnum.Initialized
    ) {
      config.modelApi.modelSpecificModelDownloadCancel({ model: model.id });
    } else if (model.downloaded) {
      CopilotLLMConfigModal.selectedModel = model.id;
      CopilotLLMConfigModal.selectedRuntime = model.cloud
        ? 'CLOUD'
        : model.cpu
        ? 'CPU'
        : 'GPU';
      PiecesDatabase.writeDB();
      Notifications.getInstance().information({
        message: `${model.foundation} ${
          model.cloud ? 'CLOUD' : model.cpu ? 'CPU' : 'GPU'
        } selected!`,
      });
    } else {
      config.modelApi.modelSpecificModelDownload({ model: model.id });
      ModelProgressController.getInstance().modelDownloadStatus.set(
        model.id,
        ModelDownloadProgressStatusEnum.InProgress
      );
    }
  }

  refresh = () => {
    this.close();
    this.open();
  };

  onClose(): void {
    ModelProgressController.getInstance().deregisterCallback(this.refresh);
  }
}
