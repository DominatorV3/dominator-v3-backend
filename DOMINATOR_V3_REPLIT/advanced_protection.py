def check_slippage(token):
  # ⚠️ En vrai, tu devrais calculer la diff entre prix achat et vente
  simulated_slippage = {
      "TOKEN333": 0.12,
      "TOKEN666": 0.42,
      "TOKEN777": 0.07,
  }
  slippage = simulated_slippage.get(token, 0.1)
  print(f"🔍 Slippage pour {token} : {slippage * 100:.1f}%")
  return slippage <= 0.25  # seuil max autorisé : 25%

def check_liquidity_lock(token):
  # ⚠️ À connecter à un scanner LP Lock comme Mudra ou DexTools API
  unlocked_liquidity = ["TOKEN666"]
  if token in unlocked_liquidity:
      print(f"🔓 LP non verrouillée pour {token}")
      return False
  print(f"🔐 LP verrouillée pour {token}")
  return True

def check_gas_estimate(token):
  # ⚠️ Ici c’est une simulation, normalement on estime via simulate_tx
  gas_map = {
      "TOKEN333": 0.00002,
      "TOKEN666": 0.004,
      "TOKEN777": 0.00003
  }
  gas = gas_map.get(token, 0.0001)
  print(f"⛽ Estimation gas pour {token} : {gas} SOL")
  return gas < 0.001  # seuil max autorisé
