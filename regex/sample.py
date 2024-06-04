
# Sample string
text = """
//+------------------------------------------------------------------+
//|                                                  LC Strategy.mq4 |
//|                                  Copyright 2024, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property strict
#property description "This EA uses just the LC indicator in its entry condition."
#property description "If there's a red LC at shift 1, a sell will get taken. If there's a green LC, a buy will get taken."
#property description "In order for this EA to work, a \"Market\" folder must exist in the Indicators folder."
#property description "Inside the Market folder, \"ML Lorentzian Classification by jdehorty.ex4\" must exist."
#property description "Netting has been added to this."

#property copyright "Samaara Das"

#include <ZonePosition.mqh>
#define ZPClass CZonePosition

string LC_PATH = "\\Market\\ML Lorentzian Classification by jdehorty.ex4";

//+------------------------------------------------------------------+
//| EA's input parameters                                            |
//+------------------------------------------------------------------+
input string  EASettings = ""; // EA's Main Settings
input bool useInitialLots = true; //Use Fixed Lots?
input double initialLots = 0.02; // Initial Lots
input bool useRiskPerEquity = false; //Use Risk as per equity?
input double riskPerEquity = 0.01; // % Risk as per equity (0.01 = 1%)
input int    _slippage = 1; // Max Slippage (in pips)
input double riskRewardRatio = 1; // Risk Reward Ratio
input int startTime = 4; // Start Hour of EA
input int endTime = 23; // End Hour of EA
input string blank1 = ""; // -
input bool allowNett = true; // Allow Netting?
input double nettRiskReward = 2; //Risk to Reward Ratio for Netting
input double nettMultiplier = 0.01; // Netting Multiplier
input int nettSlippage = 0; // Slippage for netting pending orders in pips
input double nettSwap = 0; // Swap for Netting in pips
input double nettCommission = 1; // Commission for Netting in pips
input string blank2 = ""; // -
input bool allowHardStop = false; //Allow Hard Stop?
input double hardstop = 20; //Maximum % that the balance can decrease to (for Hard Stop)
input string blank3 = ""; // -
input bool allowCutoff = true; //Allow Cut Off?
input double cutoff = 20; // Maximum % the equity can lose in a netting set (for Cut Off)
input string blank4 = ""; // -

//+------------------------------------------------------------------+
//| Indicator input parameters                                       |
//+------------------------------------------------------------------+
enum efs
{
   efs_rsi=0, //RSI
   efs_wt=1, //WT
   efs_cci=2, //CCI
   efs_adx=3, //ADX
};

input string  blank_2                 = "";              // -
input string  LCSettings              = "";              // LC Settings
input string  Input_General = "";                        // General Settings
input ENUM_APPLIED_PRICE Input_Source = PRICE_CLOSE;   // Source (Source of the input data)
input int     Input_NeighborsCount    = 8;               // Neighbors Count (Number of neighbors to consi...)
input int     Input_MaxBarsBack       = 500;             // Max Bars Back
input int     Input_FeatureCount      = 5;               // Feature (Count Number of features to use for M...)
input double  Input_ColorCompression  = 1;               // Color Compression (Compression factor for adju...)
input bool    Input_ShowDefaultExits  = true;            // Show Default Exits (Default exits occur exactly...)
input bool    Input_UseDynamicExits   = false;           // Use Dynamic Exits (Dynamic exits attempt to let...)
input bool    Input_ShowPredictionVal = false;           // Show prediction value
input string  Input_TradeStatsSettings = ""; // Trade Stats Settings
input bool    Input_ShowTradeStats    = true;            // Show Trade Stats (Displays the trade stats for a...)
input bool    Input_UseWorstCase      = false;           // Use Worst Case Estimates (Whether to use the...)
input string  Input_Filters = ""; // Filters
input bool    Input_VolatilityFilter  = true;            // Use Volatility Filter (Whether to use the volatility...)
input bool    Input_RegimeFilter      = true;            // Use Regime Filter
input bool    Input_ADXFilter         = false;           // Use ADX Filter
input double  Input_RegimeThreshold   = -0.1;            // Regime Threshold (Whether to use the trend d...)
input double  Input_ADXThreshold      = 20;              // ADX Threshold (Whether to use the ADX filter....)
input string  Input_EMAsettings = ""; // ---EMA settings
input bool    Input_UseEMAFilter      = false;           // Use EMA Filter
input int     Input_EMAPeriod         = 200;             // EMA Period (The period of the EMA used for th...)
input bool    Input_UseSMAFilter      = false;           // Use SMA Filter
input int     Input_SMAPeriod         = 200;             // Period (The period of the SMA used for the SM...)
input string  Input_NadarayaWatsonKernelRegressionSettings = ""; // Nadaraya-Watson Kernel Regression Settings
input bool    Input_TradeWithKernel   = true;            // Trade with Kernel
input bool    Input_ShowKernelEst     = true;            // Show Kemel Estimate
input bool    Input_EnhanceKernelSmth = false;           // Enhance Kernel Smoothing (Uses a crossover...)
input int     Input_LookbackWindow    = 8;               // Lookback Window (The number of bars used f...)
input double  Input_RelativeWeighting = 8.0;             // Relative Weighting (Relative weighting of time f...)
input int     Input_RegressionLevel   = 25;              // Regression Level (Bar index on which to start r...)
input int     Input_Lag               = 2;               // Lag (Lag for crossover detection. Lower values...)
input string  Input_FeatureEngineering = ""; // Feature Engineering
input efs  Input_Feature1          = efs_rsi;           // Feature 1 (The first feature to use for ML predic...)
input int     Input_Feature1_ParamA   = 14;              // Parameter A (The primary parameter of feature 1)
input int     Input_Feature1_ParamB   = 1;               // Parameter B (The secondary parameter of featu...)
input efs  Input_Feature2          = efs_wt;            // Feature 2 (The second feature to use for ML pr...)
input int     Input_Feature2_ParamA   = 10;              // Parameter A (The primary parameter of feature 2)
input int     Input_Feature2_ParamB   = 11;              // Parameter B (The secondary parameter of featu...)
input efs  Input_Feature3          = efs_cci;           // Feature 3 (The third feature to use for ML predi...)
input int     Input_Feature3_ParamA   = 20;              // Parameter A (The primary parameter of feature 3)
input int     Input_Feature3_ParamB   = 1;               // Parameter B (The secondary parameter of featu...)
input efs  Input_Feature4          = efs_adx;           // Feature 4 (The fourth feature to use for ML pre...)
input int     Input_Feature4_ParamA   = 20;              // Parameter A (The primary parameter of feature 4)
input int     Input_Feature4_ParamB   = 2;               // Parameter B (The secondary parameter of featu...)
input efs  Input_Feature5          = efs_rsi;           // Feature 5 (The fifth feature to use for ML predic...)
input int     Input_Feature5_ParamA   = 9;               // Parameter A (The primary parameter of feature 5)
input int     Input_Feature5_ParamB   = 1;               // Parameter B (The secondary parameter of featu...)
input string  Input_DisplaySettings = ""; // Display Settings
input bool    Input_ShowBarColors     = false;            // Show Bar Colors (Whether to show the bar colo...)
input bool    Input_ShowBarPredValues = false;            // Show Bar Prediction Values (Will show the ML...)
input bool    Input_UseATROffset      = false;           // Use ATR Offset (Will use the ATR offset instea...)
input double  Input_BarPredOffset     = 0;             // Bar Prediction Offset (The offset of the bar pred...)
input string  Input_Alert = ""; // Alert
input string  Input_AlertType         = "Alert";         // Alert type
input bool    Input_OpenPosSignal     = false;            // when have open position signal
input bool    Input_ClosePosSignal    = false;            // when have close position signal
input bool    Input_KernelColorChange = false;           // when Kernel color change


//+------------------------------------------------------------------+
//| Global Variables                                                 |
//+------------------------------------------------------------------+
const double BUY_SIGNAL = 1.0;
const double SELL_SIGNAL = -1.0;
ZPClass *ZonePosition; 
const double ACCT_BALANCE = AccountBalance();
double prevEquity = 0;

int OnInit()
{
   if(allowNett)
   {
     ZonePosition = new ZPClass(0.0, 0.0, nettMultiplier, 0.0, 0.0, nettSlippage); 
     ZonePosition.CalculateCutOff(allowCutoff, cutoff);
     ZonePosition.CalculateHardStop(allowHardStop, hardstop);
   }
   
   return(INIT_SUCCEEDED);
}

void OnDeinit(const int reason)
{
   if(allowNett)
   {
     delete ZonePosition;
   } 
}


void OnTick()
{

   // Getting info on the latest prices of a symbol
   MqlTick latest_price;
   SymbolInfoTick(_Symbol, latest_price);
   
   // Getting info on the date and time
   MqlDateTime date;
   TimeCurrent(date);
   
   // Handle the netting trades
   if(allowNett)
   {
      if(allowHardStop == true)
      {
        ZonePosition.SetBalanceForHardStop(ACCT_BALANCE);
        ZonePosition.CalculateHardStop(allowHardStop, hardstop); // Do not remove this. Otherwise the hard stop feature won't work. I don't know why.
      }
      
      if(allowCutoff == true)
      {
        ZonePosition.SetEquityForCutOff(prevEquity);
        ZonePosition.CalculateCutOff(allowCutoff, cutoff); // Do not remove this. Otherwise the cut off feature won't work. I don't know why.
      }
      
      ZonePosition.OnTick();     
   }
   
   // Getting the LC indicator values
   double LC = iCustom(_Symbol, PERIOD_CURRENT, LC_PATH, Input_General, Input_Source, Input_NeighborsCount, Input_MaxBarsBack, Input_FeatureCount, Input_ColorCompression, 
                        Input_ShowDefaultExits, Input_UseDynamicExits, Input_ShowPredictionVal, Input_TradeStatsSettings, Input_ShowTradeStats, Input_UseWorstCase, Input_Filters, Input_VolatilityFilter, 
                        Input_RegimeFilter, Input_ADXFilter, Input_RegimeThreshold, Input_ADXThreshold, Input_EMAsettings, Input_UseEMAFilter, Input_EMAPeriod, Input_UseSMAFilter, 
                        Input_SMAPeriod, Input_NadarayaWatsonKernelRegressionSettings, Input_TradeWithKernel, Input_ShowKernelEst, Input_EnhanceKernelSmth, Input_LookbackWindow, Input_RelativeWeighting, 
                        Input_RegressionLevel, Input_Lag, Input_FeatureEngineering, Input_Feature1, Input_Feature1_ParamA, Input_Feature1_ParamB, Input_Feature2, Input_Feature2_ParamA, 
                        Input_Feature2_ParamB, Input_Feature3, Input_Feature3_ParamA, Input_Feature3_ParamB, Input_Feature4, Input_Feature4_ParamA, Input_Feature4_ParamB, 
                        Input_Feature5, Input_Feature5_ParamA, Input_Feature5_ParamB, Input_DisplaySettings, Input_ShowBarColors, Input_ShowBarPredValues, Input_UseATROffset, Input_BarPredOffset, 
                        Input_Alert, 0, 3, 1);
   
   
   // For opening orders
   if(LC == BUY_SIGNAL)
   {
      if(hasMarketOrder() == false && date.hour >= startTime && date.hour < endTime && (!allowNett || (allowNett && ZonePosition.mHardStopHit == false)))
      {
         // Variables for sending the order
         double sl = Low[1];
         double openPrice = latest_price.ask;
         double diff = ((openPrice - sl) * riskRewardRatio);
         double lots = useInitialLots ? initialLots : useRiskPerEquity ? lotsAsPerEquity(sl, openPrice) : 0.0;
         
         prevEquity = AccountEquity();
         int pos = OrderSend(_Symbol, OP_BUY, lots, openPrice, _slippage*100, sl, openPrice+diff, "Buy");
         
         if(pos > 0) //Request is completed or order placed
         {
            Print("A buy order has been sent."); 
            if(allowNett) // Start netting if it is allowed
            {
                double high = openPrice;
                double low = sl;
                int ticket = getTicket();
                ZonePosition = new ZPClass((high - low)*nettRiskReward, high - low, nettMultiplier, nettSwap, nettCommission, _slippage);
                ZonePosition.OpenPosition(ticket);
            }
         }
         else
         {
           Print("The buy order request could not be completed - error:",GetLastError());
           ResetLastError();
         }
      }
   }
   
   if(LC == SELL_SIGNAL)
   {
      if(hasMarketOrder() == false && date.hour >= startTime && date.hour < endTime && (!allowNett || (allowNett && ZonePosition.mHardStopHit == false)))
      {
         // Variables for sending the order
         double sl = High[1];
         double openPrice = latest_price.bid;
         double diff = ((sl - openPrice) * riskRewardRatio);
         double lots = useInitialLots ? initialLots : useRiskPerEquity ? lotsAsPerEquity(sl, openPrice) : 0.0;
         
         prevEquity = AccountEquity();
         int pos = OrderSend(_Symbol, OP_SELL, lots, latest_price.bid, _slippage*100, sl, openPrice-diff, "Sell");
         
         if(pos > 0) //Request is completed or order placed
         {
            Print("A sell order has been sent."); 
            if(allowNett) // Start netting if it is allowed
            {
                double high = sl;
                double low = openPrice;
                int ticket = getTicket();
                ZonePosition = new ZPClass((high - low)*nettRiskReward, high - low, nettMultiplier, nettSwap, nettCommission, _slippage);
                ZonePosition.OpenPosition(ticket);
            }
         }
         else
         {
           Print("The sell order request could not be completed. Error:",GetLastError()," ");
           ResetLastError();
         }
      }
   }
   
}

bool hasMarketOrder() {
   for (int i=0; i < OrdersTotal(); i++) {
      if(OrderSelect(i,SELECT_BY_POS)) {
         if (OrderSymbol() == _Symbol && (OrderType()==OP_SELL || OrderType()==OP_BUY)){
            return true;
            break;
         }
      }
   }
   return false;
}

// This returns the ticket of the market order of the current symbol
int getTicket()
{
   int ticket = 0;
   for(int i = OrdersTotal()-1; i >= 0; i--)
   {
     if(OrderSelect(i, SELECT_BY_POS))
     {
       ticket = OrderTicket();
       if(OrderSymbol() == _Symbol && OrderType() <= 1) // If the order is from the current symbol and a market order
       break;
     }
   }
   return ticket;
}

// This calculates the lot size of an order based on a percentage of the equity
double lotsAsPerEquity(double sl, double entryPrice)
{
   double bid = SymbolInfoDouble(_Symbol,SYMBOL_BID); //Bid
   double point = SymbolInfoDouble(_Symbol,SYMBOL_POINT); //_Point
   double freeMargin = AccountInfoDouble(ACCOUNT_EQUITY); //double  AccountFreeMargin();
   double PipValue = ((SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE)*point) / SymbolInfoDouble(_Symbol,SYMBOL_TRADE_TICK_SIZE)); //MarketInfo(_Symbol, MODE_TICKVALUE)
   
   double pips = (sl > entryPrice ? sl - entryPrice:entryPrice - sl)/point;
   double Lots = riskPerEquity * freeMargin / (PipValue * pips);
   Lots = MathFloor(Lots * 100) / 100;
   
   return(Lots);
}    
"""

import re

def replace_value(original_text, new_value):
    """
    Replaces the value between '=' and ';' in `original_text` with `new_value`.

    Args:
        original_text (str): The original string containing the value to be replaced.
        new_value (str): The new value to insert between '=' and ';'.

    Returns:
        str: The modified string with the replaced value.

    Raises:
        ValueError: If the input string does not contain '=' and/or ';' or other errors occur.
    """
    try:
        start_index = original_text.find('=') + 1
        end_index = original_text.find(';')
        
        if start_index == 0 or end_index == -1:
            raise ValueError("The input string does not contain '=' and/or ';'")
        
        modified_string = original_text[:start_index] + new_value + original_text[end_index:]
        logger.info("Successfully replaced the value in the string.")
        
        return modified_string
    except Exception as e:
        logger.error(f"An error occurred in replace_value: {e}")
        raise

def get_property_line(text, prop, value):
    """
    Finds and replaces the value of a specific property in the given text.

    Args:
        text (str): The text to look for the property .
        prop (str): The property name to search for.
        value (str): The new value to replace the old value.

    Returns:
        str: The modified text with the replaced value, or None if the property is not found.
    """
    try:
        pattern = rf'^(input.*?;\s*//\s*{re.escape(prop)}\s*)$'
        line = re.findall(pattern, text, re.MULTILINE)
        
        if not line:
            logger.warning(f"Property '{prop}' not found in the text.")
            return None
        
        result = re.sub(pattern, replace_value(line[0], value), text, flags=re.MULTILINE)
        logger.info(f"Successfully replaced the value for property '{prop}'.")
        
        return result
    except Exception as e:
        logger.error(f"An error occurred in get_property_line: {e}")
        return None
