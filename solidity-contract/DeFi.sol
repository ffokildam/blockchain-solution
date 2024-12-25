pragma solidity ^0.8.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v4.8/contracts/token/ERC20/ERC20.sol";

contract DeFiPlatform is ERC20("DeFiPlatform", "DFP") {
    struct StakingPosition {
        uint256 positionId; // Уникальный идентификатор позиции
        address staker; // Адрес вкладчика
        uint256 amount; // Сумма токенов в стейкинге
        uint256 startDate; // Дата начала стейкинга
        uint256 durationDays; // Срок стейкинга в днях
        bool isActive; // Флаг активности позиции
    }

    struct RewardRecord {
        uint256 positionId; // Идентификатор позиции
        address staker; // Адрес вкладчика
        uint256 rewardAmount; // Сумма награды
        uint256 rewardDate; // Дата начисления награды
    }

    struct Project {
        uint256 projectId; // Уникальный идентификатор проекта
        string name; // Название проекта
        string description; // Описание проекта
        uint256 funds; // Сумма собранных средств
        address creator; // Адрес создателя проекта
    }

    address public admin;
    uint256 public nextPositionId = 1;
    uint256 public nextProjectId = 1;
    uint256 public rewardRatePerDay = 100; // Награда за день (в токенах)
    mapping(uint256 => StakingPosition) public stakingPositions; // Маппинг позиций стейкинга
    mapping(address => uint256[]) public userPositions; // Позиции для каждого пользователя
    RewardRecord[] public rewardHistory; // История всех начисленных наград
    mapping(uint256 => Project) public projects; // Маппинг проектов
    mapping(address => uint256[]) public userProjects; // Проекты, созданные пользователем

    event Staked(uint256 indexed positionId, address indexed staker, uint256 amount, uint256 startDate, uint256 durationDays);
    event Unstaked(uint256 indexed positionId, address indexed staker, uint256 rewardAmount);
    event RewardClaimed(uint256 indexed positionId, address indexed staker, uint256 rewardAmount, uint256 rewardDate);
    event ProjectCreated(uint256 indexed projectId, string name, string description, address indexed creator);
    event ProjectFunded(uint256 indexed projectId, address indexed funder, uint256 amount);
    event TokensMinted(address indexed to, uint256 amount); // Событие для эмиссии токенов

    constructor(uint256 initialSupply) {
        admin = msg.sender;
        _mint(msg.sender, initialSupply);
    }

    // Функция стейкинга
    function stake(uint256 amount, uint256 durationDays) external {
        require(amount > 0, "Amount must be greater than zero");
        require(durationDays > 0, "Duration must be greater than zero");
        require(balanceOf(msg.sender) >= amount, "Insufficient balance");

        // Трансфер токенов в контракт
        _transfer(msg.sender, address(this), amount);

        stakingPositions[nextPositionId] = StakingPosition({
            positionId: nextPositionId,
            staker: msg.sender,
            amount: amount,
            startDate: block.timestamp,
            durationDays: durationDays,
            isActive: true
        });

        userPositions[msg.sender].push(nextPositionId);

        emit Staked(nextPositionId, msg.sender, amount, block.timestamp, durationDays);
        nextPositionId++;
    }

    // Функция отзыва стейкинга
    function unstake(uint256 positionId) external {
        StakingPosition storage position = stakingPositions[positionId];
        require(position.isActive, "Position is already inactive");
        require(msg.sender == position.staker, "Only staker can unstake");
        require(block.timestamp >= position.startDate + position.durationDays * 1 days, "Staking period not yet completed");

        uint256 reward = calculateReward(position.amount, position.durationDays);
        position.isActive = false;

        // Возврат токенов и награды
        _transfer(address(this), msg.sender, position.amount + reward);

        rewardHistory.push(RewardRecord({
            positionId: positionId,
            staker: msg.sender,
            rewardAmount: reward,
            rewardDate: block.timestamp
        }));

        emit Unstaked(positionId, msg.sender, reward);
    }

    // Функция расчёта награды
    function calculateReward(uint256 amount, uint256 durationDays) public view returns (uint256) {
        return (amount * rewardRatePerDay * durationDays) / 1e18;
    }

    // Функция изменения наградного процента
    function updateRewardRate(uint256 newRate) external {
        require(msg.sender == admin, "Only admin can update reward rate");
        require(newRate > 0, "Reward rate must be greater than zero");
        rewardRatePerDay = newRate;
    }

    // Функция получения всех позиций пользователя
    function getUserPositions(address user) external view returns (uint256[] memory) {
        return userPositions[user];
    }

    // Функция начисления дополнительных токенов пользователям
    function distributeTokens(address user, uint256 amount) external {
        require(msg.sender == admin, "Only admin can distribute tokens");
        require(amount > 0, "Amount must be greater than zero");
        require(balanceOf(admin) >= amount, "Insufficient admin balance");

        _transfer(admin, user, amount);
    }

    // Функция добавления проекта
    function createProject(string memory name, string memory description) external {
        require(bytes(name).length > 0, "Project name cannot be empty");
        require(bytes(description).length > 0, "Project description cannot be empty");

        projects[nextProjectId] = Project({
            projectId: nextProjectId,
            name: name,
            description: description,
            funds: 0,
            creator: msg.sender
        });

        userProjects[msg.sender].push(nextProjectId);

        emit ProjectCreated(nextProjectId, name, description, msg.sender);
        nextProjectId++;
    }

    // Функция финансирования проекта
    function fundProject(uint256 projectId, uint256 amount) external {
        require(amount > 0, "Amount must be greater than zero");
        require(projects[projectId].creator != address(0), "Project does not exist");
        require(balanceOf(msg.sender) >= amount, "Insufficient balance");

        _transfer(msg.sender, address(this), amount);
        projects[projectId].funds += amount;

        emit ProjectFunded(projectId, msg.sender, amount);
    }

    // Функция получения списка проектов пользователя
    function getUserProjects(address user) external view returns (uint256[] memory) {
        return userProjects[user];
    }

    // Функция эмиссии новых токенов
    function mintTokens(address to, uint256 amount) external {
        require(msg.sender == admin, "Only admin can mint tokens");
        require(amount > 0, "Amount must be greater than zero");
        _mint(to, amount); // Создаём новые токены
        emit TokensMinted(to, amount); // Событие эмиссии
    }
    // Функция получения адреса админа для выполнения соответсвующих операций
    function getAdmin() public view returns (address) {
        return admin;
    }
}
