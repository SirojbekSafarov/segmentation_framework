import os.path as osp 
import time
import datetime
import torch 
from utils.torch_utils import save_on_master
from frameworks.pytorch.src.validate import validate_one_epoch, save_validation

@torch.inference_mode()
def validate(self):
    tic = time.time()
    confmat = validate_one_epoch(self._model, self._dataloader_val, device=self._device, num_classes=self._var_num_classes)

    total_time_val = str(datetime.timedelta(seconds=int(time.time() - tic)))
    print(f"** Validtaion time {total_time_val}")
    
    print(confmat, type(confmat))
    
    if self._vars.save_val_img and (self._var_current_epoch != 0 \
                        and (self._var_current_epoch%self._vars.save_val_img_freq == 0 or self._var_current_epoch == 1)):
        save_validation(self._model, self._device, self._dataset_val, self._var_num_classes, self._var_current_epoch, \
                        self._vars.val_dir, self._fn_denormalize)

    
    if self._var_current_epoch != 0 and self._var_current_epoch%self._vars.save_model_freq == 0:
        checkpoint = {
                    "self._mode_state": self._model_without_ddp.state_dict(),
                    "optimizer": self._optimizer.state_dict(),
                    "lr_scheduler": self._lr_scheduler.state_dict(),
                    "epoch": self._var_current_epoch,
                    "args": self._vars,
                    }  
        
        save_on_master(checkpoint, osp.join(self._vars.weights_dir, f"model_{self._var_current_epoch}.pth"))

    self._var_current_epoch += 1
