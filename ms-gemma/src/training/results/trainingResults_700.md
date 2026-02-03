(.venv) PS C:\Users\Usuario\Desktop\AITrain\ms-gemma\training> python .\train_lora.py            
Loading dataset from ./data/lol_coaching_enhanced_700.jsonl...
Loading model google/gemma-2-2b-it...
W0203 18:24:22.623000 16096 Lib\site-packages\torch\utils\flop_counter.py:29] triton not found; flop counting will not work for triton kernels
Loading weights:   1%|▊                                                                                 | 3/288 [00:00<00:44,  6.37it/s, Materializing param=model.layers.0.mlp.down_proj.weight]C:\Users\Usuario\Desktop\AITrain\ms-gemma\.venv\Lib\site-packages\bitsandbytes\backends\cuda\ops.py:212: FutureWarning: _check_is_size will be removed in a future PyTorch release along with guard_size_oblivious.     Use _check(i >= 0) instead.
  torch._check_is_size(blocksize)
Loading weights: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████| 288/288 [00:01<00:00, 161.62it/s, Materializing param=model.norm.weight]
Applying formatting function to train dataset: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████| 700/700 [00:00<00:00, 24047.74 examples/s]
Adding EOS to train dataset: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 700/700 [00:00<00:00, 25387.05 examples/s] 
Tokenizing train dataset: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 700/700 [00:00<00:00, 3441.60 examples/s]
Truncating train dataset: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 700/700 [00:00<00:00, 333145.67 examples/s] 
Starting training...
The tokenizer has new PAD/BOS/EOS tokens that differ from the model config and generation config. The model config and generation config were aligned accordingly, being updated with the tokenizer's values. Updated tokens: {'eos_token_id': 1}.
{'loss': '3.116', 'grad_norm': '2.094', 'learning_rate': '0.00018', 'entropy': '1.991', 'num_tokens': '1.872e+04', 'mean_token_accuracy': '0.4615', 'epoch': '0.1143'}
{'loss': '0.8248', 'grad_norm': '0.9336', 'learning_rate': '0.0001929', 'entropy': '1.017', 'num_tokens': '3.856e+04', 'mean_token_accuracy': '0.8142', 'epoch': '0.2286'}                        
{'loss': '0.2801', 'grad_norm': '0.6133', 'learning_rate': '0.000185', 'entropy': '0.2351', 'num_tokens': '5.918e+04', 'mean_token_accuracy': '0.9273', 'epoch': '0.3429'}                        
{'loss': '0.2226', 'grad_norm': '0.3047', 'learning_rate': '0.0001772', 'entropy': '0.1774', 'num_tokens': '7.884e+04', 'mean_token_accuracy': '0.9362', 'epoch': '0.4571'}                       
{'loss': '0.1894', 'grad_norm': '0.2598', 'learning_rate': '0.0001693', 'entropy': '0.1665', 'num_tokens': '9.836e+04', 'mean_token_accuracy': '0.9388', 'epoch': '0.5714'}                       
{'loss': '0.1649', 'grad_norm': '0.1787', 'learning_rate': '0.0001614', 'entropy': '0.1686', 'num_tokens': '1.18e+05', 'mean_token_accuracy': '0.9388', 'epoch': '0.6857'}                        
{'loss': '0.1462', 'grad_norm': '0.2324', 'learning_rate': '0.0001535', 'entropy': '0.1635', 'num_tokens': '1.375e+05', 'mean_token_accuracy': '0.9434', 'epoch': '0.8'}                          
{'loss': '0.1386', 'grad_norm': '0.167', 'learning_rate': '0.0001457', 'entropy': '0.1516', 'num_tokens': '1.568e+05', 'mean_token_accuracy': '0.9414', 'epoch': '0.9143'}                        
{'loss': '0.1384', 'grad_norm': '0.1797', 'learning_rate': '0.0001378', 'entropy': '0.1458', 'num_tokens': '1.76e+05', 'mean_token_accuracy': '0.9427', 'epoch': '1.023'}                         
{'loss': '0.1319', 'grad_norm': '0.1709', 'learning_rate': '0.0001299', 'entropy': '0.1359', 'num_tokens': '1.949e+05', 'mean_token_accuracy': '0.9458', 'epoch': '1.137'}                        
{'loss': '0.1376', 'grad_norm': '0.167', 'learning_rate': '0.000122', 'entropy': '0.141', 'num_tokens': '2.154e+05', 'mean_token_accuracy': '0.9434', 'epoch': '1.251'}                           
{'loss': '0.1353', 'grad_norm': '0.1387', 'learning_rate': '0.0001142', 'entropy': '0.1361', 'num_tokens': '2.353e+05', 'mean_token_accuracy': '0.9439', 'epoch': '1.366'}                        
{'loss': '0.1322', 'grad_norm': '0.127', 'learning_rate': '0.0001063', 'entropy': '0.1325', 'num_tokens': '2.545e+05', 'mean_token_accuracy': '0.9445', 'epoch': '1.48'}                          
{'loss': '0.132', 'grad_norm': '0.1523', 'learning_rate': '9.843e-05', 'entropy': '0.1349', 'num_tokens': '2.739e+05', 'mean_token_accuracy': '0.9453', 'epoch': '1.594'}                         
{'loss': '0.1332', 'grad_norm': '0.1367', 'learning_rate': '9.055e-05', 'entropy': '0.1335', 'num_tokens': '2.933e+05', 'mean_token_accuracy': '0.9446', 'epoch': '1.709'}                        
{'loss': '0.1338', 'grad_norm': '0.1021', 'learning_rate': '8.268e-05', 'entropy': '0.1329', 'num_tokens': '3.126e+05', 'mean_token_accuracy': '0.9448', 'epoch': '1.823'}                        
{'loss': '0.1385', 'grad_norm': '0.1533', 'learning_rate': '7.48e-05', 'entropy': '0.1377', 'num_tokens': '3.329e+05', 'mean_token_accuracy': '0.9419', 'epoch': '1.937'}                         
{'loss': '0.1317', 'grad_norm': '0.1934', 'learning_rate': '6.693e-05', 'entropy': '0.1339', 'num_tokens': '3.513e+05', 'mean_token_accuracy': '0.9465', 'epoch': '2.046'}                        
{'loss': '0.1333', 'grad_norm': '0.1289', 'learning_rate': '5.906e-05', 'entropy': '0.1339', 'num_tokens': '3.711e+05', 'mean_token_accuracy': '0.9442', 'epoch': '2.16'}                         
{'loss': '0.1308', 'grad_norm': '0.1328', 'learning_rate': '5.118e-05', 'entropy': '0.1328', 'num_tokens': '3.905e+05', 'mean_token_accuracy': '0.9443', 'epoch': '2.274'}                        
{'loss': '0.1289', 'grad_norm': '0.1523', 'learning_rate': '4.331e-05', 'entropy': '0.132', 'num_tokens': '4.095e+05', 'mean_token_accuracy': '0.9464', 'epoch': '2.389'}                         
{'loss': '0.1324', 'grad_norm': '0.1406', 'learning_rate': '3.543e-05', 'entropy': '0.1336', 'num_tokens': '4.295e+05', 'mean_token_accuracy': '0.9459', 'epoch': '2.503'}                        
{'loss': '0.1307', 'grad_norm': '0.1406', 'learning_rate': '2.756e-05', 'entropy': '0.131', 'num_tokens': '4.489e+05', 'mean_token_accuracy': '0.9461', 'epoch': '2.617'}                         
{'loss': '0.1315', 'grad_norm': '0.1318', 'learning_rate': '1.969e-05', 'entropy': '0.1318', 'num_tokens': '4.684e+05', 'mean_token_accuracy': '0.9442', 'epoch': '2.731'}                        
{'loss': '0.1363', 'grad_norm': '0.1436', 'learning_rate': '1.181e-05', 'entropy': '0.1371', 'num_tokens': '4.891e+05', 'mean_token_accuracy': '0.942', 'epoch': '2.846'}                         
{'loss': '0.1328', 'grad_norm': '0.1357', 'learning_rate': '3.937e-06', 'entropy': '0.1337', 'num_tokens': '5.089e+05', 'mean_token_accuracy': '0.9447', 'epoch': '2.96'}                         
{'train_runtime': '1575', 'train_samples_per_second': '1.333', 'train_steps_per_second': '0.168', 'train_loss': '0.2854', 'entropy': '0.1267', 'num_tokens': '5.153e+05', 'mean_token_accuracy': '0.9473', 'epoch': '3'}
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 264/264 [26:15<00:00,  5.97s/it] 
Saving model to ../models/gemma_lora_output...
Training complete!