(.venv) PS C:\Users\Usuario\Desktop\AITrain\ms-gemma\training> python .\train_lora.py
Loading dataset from ./data/train.jsonl...
Loading model google/gemma-2-2b-it...
W0203 12:19:51.326000 18912 Lib\site-packages\torch\utils\flop_counter.py:29] triton not found; flop counting will not work for triton kernels
Loading weights:   1%|▉                                                                                            | 3/288 [00:00<01:43,  2.75it/s, Materializing param=model.layers.0.mlp.down_proj.weight]C:\Users\Usuario\Desktop\AITrain\ms-gemma\.venv\Lib\site-packages\bitsandbytes\backends\cuda\ops.py:212: FutureWarning: _check_is_size will be removed in a future PyTorch release along with guard_size_oblivious.     Use _check(i >= 0) instead.
  torch._check_is_size(blocksize)
Loading weights: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████| 288/288 [00:03<00:00, 81.24it/s, Materializing param=model.norm.weight]
Applying formatting function to train dataset: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 350/350 [00:00<00:00, 17439.73 examples/s]
Adding EOS to train dataset: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 350/350 [00:00<00:00, 18084.69 examples/s] 
Tokenizing train dataset: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 350/350 [00:00<00:00, 3645.69 examples/s]
Truncating train dataset: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 350/350 [00:00<00:00, 172584.81 examples/s] 
Starting training...
The tokenizer has new PAD/BOS/EOS tokens that differ from the model config and generation config. The model config and generation config were aligned accordingly, being updated with the tokenizer's values. Updated tokens: {'eos_token_id': 1}.
{'loss': '3.15', 'grad_norm': '2.219', 'learning_rate': '0.00018', 'entropy': '2.065', 'num_tokens': '1.822e+04', 'mean_token_accuracy': '0.4662', 'epoch': '0.2286'}
{'loss': '1.084', 'grad_norm': '1.289', 'learning_rate': '0.0001852', 'entropy': '1.258', 'num_tokens': '3.646e+04', 'mean_token_accuracy': '0.7754', 'epoch': '0.4571'}                                     
{'loss': '0.4976', 'grad_norm': '1.156', 'learning_rate': '0.0001689', 'entropy': '0.4511', 'num_tokens': '5.477e+04', 'mean_token_accuracy': '0.872', 'epoch': '0.6857'}                                    
{'loss': '0.2939', 'grad_norm': '0.9766', 'learning_rate': '0.0001525', 'entropy': '0.2593', 'num_tokens': '7.276e+04', 'mean_token_accuracy': '0.914', 'epoch': '0.9143'}                                   
{'loss': '0.2401', 'grad_norm': '0.6875', 'learning_rate': '0.0001361', 'entropy': '0.2149', 'num_tokens': '9.019e+04', 'mean_token_accuracy': '0.9221', 'epoch': '1.137'}                                   
{'loss': '0.2125', 'grad_norm': '0.4883', 'learning_rate': '0.0001197', 'entropy': '0.2053', 'num_tokens': '1.087e+05', 'mean_token_accuracy': '0.923', 'epoch': '1.366'}                                    
{'loss': '0.1933', 'grad_norm': '0.4688', 'learning_rate': '0.0001033', 'entropy': '0.1973', 'num_tokens': '1.272e+05', 'mean_token_accuracy': '0.9203', 'epoch': '1.594'}                                   
{'loss': '0.179', 'grad_norm': '0.4043', 'learning_rate': '8.689e-05', 'entropy': '0.1982', 'num_tokens': '1.454e+05', 'mean_token_accuracy': '0.9284', 'epoch': '1.823'}                                    
{'loss': '0.1635', 'grad_norm': '0.4141', 'learning_rate': '7.049e-05', 'entropy': '0.1855', 'num_tokens': '1.626e+05', 'mean_token_accuracy': '0.9328', 'epoch': '2.046'}                                   
{'loss': '0.1636', 'grad_norm': '0.418', 'learning_rate': '5.41e-05', 'entropy': '0.1842', 'num_tokens': '1.81e+05', 'mean_token_accuracy': '0.9296', 'epoch': '2.274'}                                      
{'loss': '0.1589', 'grad_norm': '0.3652', 'learning_rate': '3.77e-05', 'entropy': '0.1763', 'num_tokens': '1.991e+05', 'mean_token_accuracy': '0.9322', 'epoch': '2.503'}                                    
{'loss': '0.1531', 'grad_norm': '0.3848', 'learning_rate': '2.131e-05', 'entropy': '0.1695', 'num_tokens': '2.168e+05', 'mean_token_accuracy': '0.9334', 'epoch': '2.731'}                                   
{'loss': '0.16', 'grad_norm': '0.3281', 'learning_rate': '4.918e-06', 'entropy': '0.1765', 'num_tokens': '2.353e+05', 'mean_token_accuracy': '0.9298', 'epoch': '2.96'}                                      
{'train_runtime': '296.9', 'train_samples_per_second': '3.537', 'train_steps_per_second': '0.445', 'train_loss': '0.5062', 'entropy': '0.1821', 'num_tokens': '2.386e+05', 'mean_token_accuracy': '0.9303', 'epoch': '3'}
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 132/132 [04:56<00:00,  2.25s/it] 
Saving model to ../models/gemma_lora_output...
Training complete!