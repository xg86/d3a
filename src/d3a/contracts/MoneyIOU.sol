pragma solidity ^0.4.4;
import "IOUToken.sol";
contract MoneyIOU is IOUToken{
    address approver;

    mapping (address => uint256) allowedMarkets;

    address[] markets;

    function MoneyIOU(
      uint128 _initialAmount,
      string _tokenName,
      uint8 _decimalUnits,
      string _tokenSymbol
      ) IOUToken (
          _initialAmount,
          _tokenName,
          _decimalUnits,
          _tokenSymbol
      ){
        approver = msg.sender;
    }

    function marketTransfer(address _from, address _to, uint256 _value) returns (bool success) {
        // 1st condition checks whether market is registered and
        // second condition checks whether _value is below the allowed value for transfers
        if (allowedMarkets[msg.sender] > 0 && _value < allowedMarkets[msg.sender] && _value > 0) {
            balances[_to] += int(_value);
            balances[_from] -= int(_value);
            success = true;
        }
        else {
            success = false;
        }
    }

    function globallyApprove(uint _value) returns (bool success) {
        if (tx.origin == approver && _value > 0) {
            allowedMarkets[msg.sender] = _value;
            markets.push(msg.sender);
            success = true;
        }
        else {
            success = false;
        }
    }

    function isGloballyApproved(address _market) constant returns (bool) {
        return allowedMarkets[_market] > 0;
    }

    function getApprover() constant returns (address) {
        return approver;
    }

    function getApprovedMarkets() constant returns (address[]) {
        return markets;
    }

}
